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


import json
import copy
import json
from flask import render_template, abort, request, url_for, redirect, g
from flask.ext.babel import gettext
import time
import datetime

from rrd import app
from rrd.model.screen import DashboardScreen
from rrd.model.graph import DashboardGraph
from rrd import consts
from rrd.utils.graph_urls import generate_graph_urls 
from rrd import config

@app.route("/screen", methods=["GET", "POST"])
def dash_screens():
    top_screens = DashboardScreen.gets_by_pid(pid='0') or []
    top_screens = sorted(top_screens, key=lambda x:x.name)

    return render_template("screen/index.html", **locals())

@app.route("/screen/<int:sid>/delete")
def dash_screen_delete(sid):
    screen = DashboardScreen.get(sid)
    if not screen:
        abort(404, "no such screen")
    DashboardScreen.remove(sid)

    return redirect("/screen")

@app.route("/screen/<int:sid>/edit", methods=["GET", "POST"])
def dash_screen_edit(sid):
    screen = DashboardScreen.get(sid)
    if not screen:
        abort(404, "no such screen")

    if request.method == "POST":
        screen_name = request.form.get("screen_name")
        screen.update(name=screen_name)
        return redirect("/screen/%s" %screen.id)
    else:
        return render_template("screen/edit.html", **locals())

@app.route("/screen/<int:sid>/clone", methods=["GET", "POST"])
def dash_screen_clone(sid):
    screen = DashboardScreen.get(sid)
    if not screen:
        abort(404, "no such screen")

    if request.method == "POST":
        screen_name = request.form.get("screen_name")
        with_graph = request.form.get("with_graph")

        new_s = DashboardScreen.add(screen.pid, screen_name)
        if not new_s:
            abort(404, gettext("screen create fail"))

        if with_graph:
            old_graphs = DashboardGraph.gets_by_screen_id(sid)
            for o in old_graphs:
                DashboardGraph.add(o.title, o.hosts, o.counters, new_s.id,
                        o.timespan, o.graph_type, o.method, o.position)

        return redirect("/screen/%s" %new_s.id)
    else:
        return render_template("screen/clone.html", **locals())

@app.route("/graph/<int:gid>/delete")
def dash_graph_delete(gid):
    graph = DashboardGraph.get(gid)
    if not graph:
        abort(404, "no such graph")
    DashboardGraph.remove(gid)
    return redirect("/screen/" + graph.screen_id)

@app.route("/screen/<int:sid>")
def dash_screen(sid):
    start = request.args.get("start")
    end = request.args.get("end")

    top_screens = DashboardScreen.gets_by_pid(pid=0)
    top_screens = sorted(top_screens, key=lambda x:x.name)

    screen = DashboardScreen.get(sid)
    if not screen:
        abort(404, "no screen")

    if str(screen.pid) == '0':
        sub_screens = DashboardScreen.gets_by_pid(pid=sid)
        sub_screens = sorted(sub_screens, key=lambda x:x.name)
        return render_template("screen/top_screen.html", **locals())

    pscreen = DashboardScreen.get(screen.pid)
    sub_screens = DashboardScreen.gets_by_pid(pid=screen.pid)
    sub_screens = sorted(sub_screens, key=lambda x:x.name)
    graphs = DashboardGraph.gets_by_screen_id(screen.id)

    all_graphs = []

    for graph in graphs:
        all_graphs.extend(generate_graph_urls(graph, start, end) or [])

    all_graphs = sorted(all_graphs, key=lambda x:x.position)

    return render_template("screen/screen.html", **locals())

@app.route("/screen/embed/<int:sid>")
def dash_screen_embed(sid):
    start = request.args.get("start")
    end = request.args.get("end")

    screen = DashboardScreen.get(sid)
    if not screen:
        abort(404, "no screen")

    if screen.pid == '0':
        abort(404, "top screen")

    graphs = DashboardGraph.gets_by_screen_id(screen.id)
    all_graphs = []

    for graph in graphs:
        all_graphs.extend(generate_graph_urls(graph, start, end) or [])

    all_graphs = sorted(all_graphs, key=lambda x:x.position)

    return render_template("screen/screen_embed.html", **locals())


@app.route("/screen/add", methods=["GET", "POST"])
def dash_screen_add():
    if request.method == "POST":
        name = request.form.get("screen_name")
        pid = request.form.get("pid", '0')
        screen = DashboardScreen.add(pid, name)
        return redirect("/screen/%s" % screen.id)
    else:
        pid = request.args.get("pid", '0')
        try:
            screen = DashboardScreen.get(pid)
        except:
            screen = None
        return render_template("screen/add.html", **locals())

@app.route("/screen/<int:sid>/graph", methods=["GET", "POST"])
def dash_graph_add(sid):
    all_screens = DashboardScreen.gets_all()
    top_screens = [x for x in all_screens if x.pid == '0']
    children = []
    for t in top_screens:
        children.append([x for x in all_screens if x.pid == t.id])

    screen = DashboardScreen.get(sid)
    if not screen:
        abort(404, "no screen")
    pscreen = DashboardScreen.get(screen.pid)

    if request.method == "POST":
        title = request.form.get("title")

        hosts = request.form.get("hosts", "").strip()
        hosts = hosts and hosts.split("\n") or []
        hosts = [x.strip() for x in hosts]

        counters = request.form.get("counters", "").strip()
        counters = counters and counters.split("\n") or []
        counters = [x.strip() for x in counters]

        timespan = int(request.form.get("timespan", 3600))
        graph_type = request.form.get("graph_type", 'h')
        method = request.form.get("method", '').upper()
        position = int(request.form.get("position", 0))

        graph = DashboardGraph.add(title, hosts, counters, sid,
                timespan, graph_type, method, position)
        return redirect("/screen/%s" % sid)

    else:
        gid = request.args.get("gid")
        graph = gid and DashboardGraph.get(gid)
        return render_template("screen/graph_add.html", config=config, **locals())

@app.route("/graph/<int:gid>/edit", methods=["GET", "POST"])
def dash_graph_edit(gid):
    error = ""
    graph = DashboardGraph.get(gid)
    if not graph:
        abort(404, "no graph")

    all_screens = DashboardScreen.gets_all()
    top_screens = [x for x in all_screens if x.pid == '0']
    children = []
    for t in top_screens:
        children.append([x for x in all_screens if x.pid == t.id])

    screen = DashboardScreen.get(graph.screen_id)
    if not screen:
        abort(404, "no screen")
    pscreen = DashboardScreen.get(screen.pid)

    if request.method == "POST":
        ajax = request.form.get("ajax", "")
        screen_id = request.form.get("screen_id")
        title = request.form.get("title", "").strip()

        hosts = request.form.get("hosts", "").strip()
        hosts = hosts and hosts.split("\n") or []
        hosts = [x.strip() for x in hosts]

        counters = request.form.get("counters", "").strip()
        counters = counters and counters.split("\n") or []
        counters = [x.strip() for x in counters]

        timespan = request.form.get("timespan", 3600)
        graph_type = request.form.get("graph_type", 'h')
        method = request.form.get("method", '').upper()
        position = request.form.get("position", 0)

        graph = graph.update(title, hosts, counters, screen_id,
                timespan, graph_type, method, position)

        error = gettext("edit successful")
        if not ajax:
            return render_template("screen/graph_edit.html", config=config, **locals())
        else:
            return "ok"

    else:
        ajax = request.args.get("ajax", "")
        return render_template("screen/graph_edit.html", **locals())

@app.route("/graph/multi_edit", methods=["GET", "POST"])
def dash_graph_multi_edit():
    ret = {
            "ok": False,
            "msg": "",
            "data": [],
    }
    if request.method == "POST":
        d = request.data
        try:
            jdata = json.loads(d)
        except ValueError:
            jdata = None

        if not jdata:
            return json.dumps({
                    "ok": False,
                    "msg": "no_data_post",
            })
        rows = []
        for x in jdata:
            rows.append({"id": x["id"], "hosts": x["endpoints"], "counters": x["counters"]})
        DashboardGraph.update_multi(rows) 

        return json.dumps({
             "ok": True,
             "msg": "",
        })
        
    elif request.method == "GET":
        sid = request.args.get("sid")
        if not sid or not DashboardScreen.get(sid):
            ret["msg"] = "no_screen"
            return json.dumps(ret)
        
        ret["ok"] = True
        graphs = DashboardGraph.gets_by_screen_id(sid)
        ret['data'] = [{"id": x.id, "title": x.title, "endpoints":x.hosts, "counters":x.counters} for x in graphs]
        return json.dumps(ret)
    
