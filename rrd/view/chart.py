#-*- coding:utf-8 -*-
import os
import time
import datetime
import socket
import hashlib
import random
import urllib
import json
import random
from flask import request, g, abort, render_template
from MySQLdb import ProgrammingError

from rrd import app
from rrd.consts import RRD_CFS, GRAPH_TYPE_KEY, GRAPH_TYPE_HOST
from rrd.model.graph import TmpGraph
from rrd.utils.rrdgraph import merge_list
from rrd.utils.rrdgraph import graph_query

@app.teardown_request
def teardown_request(exception):
    from rrd.store import dashboard_db_conn as db_conn
    try:
        db_conn and db_conn.commit()
    except ProgrammingError:
        pass

    from rrd.store import graph_db_conn
    try:
        graph_db_conn and graph_db_conn.commit()
    except ProgrammingError:
        pass
#
@app.before_request
def chart_before():
    if request.method == "GET":
        now = int(time.time())

        #是否显示顶部图表导航
        g.nav_header = request.args.get("nav_header") or "on"
        g.cols = request.args.get("cols") or "2"
        try:
            g.cols = int(g.cols)
        except:
            g.cols = 2
        if g.cols <= 0:
            g.cols = 2
        if g.cols >= 6:
            g.cols = 6

        g.legend = request.args.get("legend") or "off"
        g.graph_type = request.args.get("graph_type") or GRAPH_TYPE_HOST
        g.sum = request.args.get("sum") or "off" #是否求和
        g.sumonly = request.args.get("sumonly") or "off" #是否只显示求和

        g.cf = (request.args.get("cf") or "AVERAGE").upper() # MAX, MIN, AVGRAGE, LAST

        g.start = int(request.args.get("start") or -3600)
        if g.start < 0:
            g.start = now + g.start

        g.end = int(request.args.get("end") or 0)
        if g.end <= 0:
            g.end = now + g.end
        g.end = g.end - 60

        g.id = request.args.get("id") or ""

        g.limit = int(request.args.get("limit") or 0)
        g.page = int(request.args.get("page") or 0)

@app.route("/chart", methods=["POST",])
def chart():
    endpoints = request.form.getlist("endpoints[]") or []
    counters = request.form.getlist("counters[]") or []
    graph_type = request.form.get("graph_type") or GRAPH_TYPE_HOST

    id_ = TmpGraph.add(endpoints, counters)

    ret = {
            "ok": False,
            "id": id_,
            "params": {
                "graph_type": graph_type,
            },
    }
    if id_:
        ret['ok'] = True

    return json.dumps(ret)

@app.route("/chart/big", methods=["GET",])
def chart_big():
    return render_template("chart/big_ng.html", **locals())

@app.route("/chart/embed", methods=["GET",])
def chart_embed():
    w = request.args.get("w")
    w = int(w) if w else 600
    h = request.args.get("h")
    h = int(h) if h else 200
    return render_template("chart/embed.html", **locals())

@app.route("/chart/h", methods=["GET"])
def multi_endpoints_chart_data():
    if not g.id:
        abort(400, "no graph id given")

    tmp_graph = TmpGraph.get(g.id)
    if not tmp_graph:
        abort(404, "no graph which id is %s" %g.id)

    counters = tmp_graph.counters
    if not counters:
        abort(400, "no counters of %s" %g.id)
    counters = sorted(set(counters))

    endpoints = tmp_graph.endpoints
    if not endpoints:
        abort(400, "no endpoints of %s" %(g.id,))
    endpoints = sorted(set(endpoints))

    ret = {
        "units": "",
        "title": "",
        "series": []
    }
    ret['title'] = counters[0]
    c = counters[0]
    endpoint_counters = []
    for e in endpoints:
        endpoint_counters.append({
            "endpoint": e,
            "counter": c,
        })

    query_result = graph_query(endpoint_counters, g.cf, g.start, g.end)

    series = []
    for i in range(0, len(query_result)):
        x = query_result[i]
        try:
            xv = [(v["timestamp"]*1000, v["value"]) for v in x["Values"]]
            serie = {
                    "data": xv,
                    "name": query_result[i]["endpoint"],
                    "cf": g.cf,
                    "endpoint": query_result[i]["endpoint"],
                    "counter": query_result[i]["counter"],
            }
            series.append(serie)
        except:
            pass

    sum_serie = {
            "data": [],
            "name": "sum",
            "cf": g.cf,
            "endpoint": "sum",
            "counter": c,
    }
    if g.sum == "on" or g.sumonly == "on":
        sum = []
        tmp_ts = []
        max_size = 0
        for serie in series:
            serie_vs = [x[1] for x in serie["data"]]
            if len(serie_vs) > max_size:
                max_size = len(serie_vs)
                tmp_ts = [x[0] for x in serie["data"]]
            sum = merge_list(sum, serie_vs)
        sum_serie_data = []
        for i in range(0, max_size):
            sum_serie_data.append((tmp_ts[i], sum[i]))
        sum_serie['data'] = sum_serie_data

        series.append(sum_serie)

    if g.sumonly == "on":
        ret['series'] = [sum_serie,]
    else:
        ret['series'] = series

    return json.dumps(ret)

@app.route("/chart/k", methods=["GET"])
def multi_counters_chart_data():
    if not g.id:
        abort(400, "no graph id given")

    tmp_graph = TmpGraph.get(g.id)
    if not tmp_graph:
        abort(404, "no graph which id is %s" %g.id)

    counters = tmp_graph.counters
    if not counters:
        abort(400, "no counters of %s" %g.id)
    counters = sorted(set(counters))

    endpoints = tmp_graph.endpoints
    if not endpoints:
        abort(400, "no endpoints of %s" % g.id)
    endpoints = sorted(set(endpoints))

    ret = {
        "units": "",
        "title": "",
        "series": []
    }
    ret['title'] = endpoints[0]
    e = endpoints[0]
    endpoint_counters = []
    for c in counters:
        endpoint_counters.append({
            "endpoint": e,
            "counter": c,
        })

    query_result = graph_query(endpoint_counters, g.cf, g.start, g.end)

    series = []
    for i in range(0, len(query_result)):
        x = query_result[i]
        try:
            xv = [(v["timestamp"]*1000, v["value"]) for v in x["Values"]]
            serie = {
                    "data": xv,
                    "name": query_result[i]["counter"],
                    "cf": g.cf,
                    "endpoint": query_result[i]["endpoint"],
                    "counter": query_result[i]["counter"],
            }
            series.append(serie)
        except:
            pass

    sum_serie = {
            "data": [],
            "name": "sum",
            "cf": g.cf,
            "endpoint": e,
            "counter": "sum",
    }
    if g.sum == "on" or g.sumonly == "on":
        sum = []
        tmp_ts = []
        max_size = 0
        for serie in series:
            serie_vs = [x[1] for x in serie["data"]]
            if len(serie_vs) > max_size:
                max_size = len(serie_vs)
                tmp_ts = [x[0] for x in serie["data"]]
            sum = merge_list(sum, serie_vs)
        sum_serie_data = []
        for i in range(0, max_size):
            sum_serie_data.append((tmp_ts[i], sum[i]))
        sum_serie['data'] = sum_serie_data

        series.append(sum_serie)

    if g.sumonly == "on":
        ret['series'] = [sum_serie,]
    else:
        ret['series'] = series

    return json.dumps(ret)

@app.route("/chart/a", methods=["GET"])
def multi_chart_data():
    if not g.id:
        abort(400, "no graph id given")

    tmp_graph = TmpGraph.get(g.id)
    if not tmp_graph:
        abort(404, "no graph which id is %s" %g.id)

    counters = tmp_graph.counters
    if not counters:
        abort(400, "no counters of %s" %g.id)
    counters = sorted(set(counters))

    endpoints = tmp_graph.endpoints
    if not endpoints:
        abort(400, "no endpoints of %s, and tags:%s" %(g.id, g.tags))
    endpoints = sorted(set(endpoints))

    ret = {
        "units": "",
        "title": "",
        "series": []
    }

    endpoint_counters = []
    for e in endpoints:
        for c in counters:
            endpoint_counters.append({
                "endpoint": e,
                "counter": c,
            })
    query_result = graph_query(endpoint_counters, g.cf, g.start, g.end)

    series = []
    for i in range(0, len(query_result)):
        x = query_result[i]
        try:
            xv = [(v["timestamp"]*1000, v["value"]) for v in x["Values"]]
            serie = {
                    "data": xv,
                    "name": "%s %s" %(query_result[i]["endpoint"], query_result[i]["counter"]),
                    "cf": g.cf,
                    "endpoint": "",
                    "counter": "",
            }
            series.append(serie)
        except:
            pass

    sum_serie = {
            "data": [],
            "name": "sum",
            "cf": g.cf,
            "endpoint": "",
            "counter": "",
    }
    if g.sum == "on" or g.sumonly == "on":
        sum = []
        tmp_ts = []
        max_size = 0
        for serie in series:
            serie_vs = [x[1] for x in serie["data"]]
            if len(serie_vs) > max_size:
                max_size = len(serie_vs)
                tmp_ts = [x[0] for x in serie["data"]]
            sum = merge_list(sum, serie_vs)
        sum_serie_data = []
        for i in range(0, max_size):
            sum_serie_data.append((tmp_ts[i], sum[i]))
        sum_serie['data'] = sum_serie_data

        series.append(sum_serie)

    if g.sumonly == "on":
        ret['series'] = [sum_serie,]
    else:
        ret['series'] = series

    return json.dumps(ret)

@app.route("/charts", methods=["GET"])
def charts():
    if not g.id:
        abort(400, "no graph id given")

    tmp_graph = TmpGraph.get(g.id)
    if not tmp_graph:
        abort(404, "no graph which id is %s" %g.id)

    counters = tmp_graph.counters
    if not counters:
        abort(400, "no counters of %s" %g.id)
    counters = sorted(set(counters))

    endpoints = tmp_graph.endpoints
    if not endpoints:
        abort(400, "no endpoints of %s" %g.id)
    endpoints = sorted(set(endpoints))

    chart_urls = []
    chart_ids = []
    p = {
        "id": "",
        "legend": g.legend,
        "cf": g.cf,
        "sum": g.sum,
        "graph_type": g.graph_type,
        "nav_header": g.nav_header,
        "start": g.start,
        "end": g.end,
    }

    if g.graph_type == GRAPH_TYPE_KEY:

        for x in endpoints:
            id_ = TmpGraph.add([x], counters)
            if not id_:
                continue

            p["id"] = id_
            chart_ids.append(int(id_))
            src = "/chart/h?" + urllib.urlencode(p)
            chart_urls.append(src)
    elif g.graph_type == GRAPH_TYPE_HOST:
        for x in counters:
            id_ = TmpGraph.add(endpoints, [x])
            if not id_:
                continue
            p["id"] = id_
            chart_ids.append(int(id_))
            src = "/chart/h?" + urllib.urlencode(p)
            chart_urls.append(src)
    else:
        id_ = TmpGraph.add(endpoints, counters)
        if id_:
            p["id"] = id_
            chart_ids.append(int(id_))
            src = "/chart/a?" + urllib.urlencode(p)
            chart_urls.append(src)

    return render_template("chart/multi_ng.html", **locals())

