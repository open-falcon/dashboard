#-*- coding:utf-8 -*-
# Copyright 2017 Xiaomi, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import urllib
import json
from flask import request, g, abort, render_template

from rrd import app
from rrd.consts import GRAPH_TYPE_KEY, GRAPH_TYPE_HOST
from rrd.utils.rrdgraph import merge_list
from rrd.utils.rrdgraph import graph_history
from rrd.model.tmpgraph import TmpGraph

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
    if id_: ret['ok'] = True

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

    j = TmpGraph.get(g.id)
    if not j:
        abort(400, "no such tmp_graph where id=%s" %g.id)

    counters = j.counters
    if not counters:
        abort(400, "no counters of %s" %g.id)
    counters = sorted(set(counters))

    endpoints = j.endpoints
    if not endpoints:
        abort(400, "no endpoints of %s" %(g.id,))
    endpoints = sorted(set(endpoints))

    ret = {
        "units": "",
        "title": "",
        "series": []
   }

    c = counters[0]
    ret['title'] = c
    query_result = graph_history(endpoints, counters[:1], g.cf, g.start, g.end)

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

    j = TmpGraph.get(g.id)
    if not j:
        abort(400, "no such tmp_graph where id=%s" %g.id)

    counters = j.counters
    if not counters:
        abort(400, "no counters of %s" %g.id)
    counters = sorted(set(counters))

    endpoints = j.endpoints
    if not endpoints:
        abort(400, "no endpoints of %s" % g.id)
    endpoints = sorted(set(endpoints))

    ret = {
        "units": "",
        "title": "",
        "series": []
    }
    e = endpoints[0]
    ret['title'] = e

    query_result = graph_history(endpoints[:1], counters, g.cf, g.start, g.end)

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

    j = TmpGraph.get(g.id)
    if not j:
        abort(400, "no such tmp_graph where id=%s" %g.id)

    counters = j.counters
    if not counters:
        abort(400, "no counters of %s" %g.id)
    counters = sorted(set(counters))

    endpoints = j.endpoints
    if not endpoints:
        abort(400, "no endpoints of %s, and tags:%s" %(g.id, g.tags))
    endpoints = sorted(set(endpoints))

    ret = {
        "units": "",
        "title": "",
        "series": []
    }

    query_result = graph_history(endpoints, counters, g.cf, g.start, g.end)

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

    j = TmpGraph.get(g.id)
    if not j:
        abort(400, "no such tmp_graph where id=%s" %g.id)

    counters = j.counters
    if not counters:
        abort(400, "no counters of %s" %g.id)
    counters = sorted(set(counters))

    endpoints = j.endpoints
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
