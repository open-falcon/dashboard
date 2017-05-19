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
import re
from flask import request, abort, g, render_template
from rrd import app, config
from rrd import corelib


def get_api_endpoints(q, tags, page=1, limit=100):
    if not q and not tags:
        raise Exception("no query params given")

    h = {"Content-type": "application/json"}
    r = corelib.auth_requests("GET", config.API_ADDR + "/graph/endpoint?q=%s&limit=%d&page=%d&tags=%s" %(q, limit, page, tags), headers=h)
    if r.status_code != 200:
        raise Exception(r.text)

    j = sorted(r.json(), key=lambda x:x["endpoint"])

    return j


@app.route("/")
def index():
    q = request.args.get("q") or "."
    raw_tag = request.args.get("tags") or ""
    tags = ','.join(re.split('\s*,\s*', raw_tag))
    limit = int(request.args.get("limit") or 50)
    page = int(request.args.get("page") or 1)

    endpoint_objs = get_api_endpoints(q, tags, page, limit)
    return render_template("index.html", **locals())

@app.route("/api/endpoints")
def api_endpoints():
    ret = {
            "ok": False,
            "msg": "",
            "data": [],
            }

    q = request.args.get("q") or "."
    raw_tag = request.args.get("tags") or ""
    tags = ','.join(re.split('\s*,\s*', raw_tag))
    limit = int(request.args.get("limit") or 100)
    page = int(request.args.get("page") or 1)

    try:
        data = get_api_endpoints(q, tags, page, limit)
        ret['data'] = data
        ret['ok'] = True
        return json.dumps(ret)
    except Exception as e:
        abort(400, str(ret))

@app.route("/api/counters", methods=["POST"])
def api_get_counters():
    ret = {
            "ok": False,
            "msg": "",
            "data": [],
            }

    q = request.form.get("q") or ""
    limit = int(request.form.get("limit") or 50)
    page = int(request.form.get("page") or 1)
    eids = request.form.get("eids") or ""
    eids = eids and json.loads(eids) or []

    if not (eids or q):
        ret['msg'] = "no endpoints or counter given"
        return json.dumps(ret)


    h = {"Content-type": "application/json"}
    r = corelib.auth_requests("GET", config.API_ADDR + "/graph/endpoint_counter?eid=%s&metricQuery=%s&limit=%d&page=%d" %(",".join(eids), q, limit, page), headers=h)
    if r.status_code != 200:
        abort(400, r.text)
    j = r.json()

    counters_map = {}
    for x in j:
        counters_map[x['counter']] = [x['counter'], x['type'], x['step']]
    sorted_counters = sorted(counters_map.keys())
    sorted_values = [counters_map[x] for x in sorted_counters]

    ret['data'] = sorted_values
    ret['ok'] = True

    return json.dumps(ret)


@app.route("/api/counters", methods=["DELETE"])
def api_delete_counters():
    ret = {
            "ok": False,
            "msg": "",
    }

    endpoints = request.form.getlist("endpoints[]") or []
    counters = request.form.getlist("counters[]") or []
    if len(endpoints) == 0 or len(counters) == 0:
        ret['msg'] = "no endpoint and counter"
        return json.dumps(ret)

    h = {"Content-type": "application/json"}
    d = {
            "endpoints": endpoints,
            "counters": counters,
    }
    r = corelib.auth_requests("DELETE", config.API_ADDR + "/graph/counter", headers=h, data=json.dumps(d))
    if r.status_code != 200:
        abort(r.status_code, r.text)
    j = r.json()

    ret["ok"] = True
    ret["data"] = "%s counters affected" %j.get("affected_counter")
    return json.dumps(ret)


@app.route("/api/endpoints", methods=["DELETE"])
def api_delete_endpoints():
    ret = {
            "ok": False,
            "msg": "",
    }

    endpoints = request.form.getlist("endpoints[]") or []
    if len(endpoints) == 0:
        ret['msg'] = "no endpoint"
        return json.dumps(ret)

    h = {"Content-type": "application/json"}
    d = endpoints

    r = corelib.auth_requests("DELETE", config.API_ADDR + "/graph/endpoint", headers=h, data=json.dumps(d))
    if r.status_code != 200:
        abort(r.status_code, r.text)
    j = r.json()

    ret["ok"] = True
    ret["data"] = "%s counters affected, %s endpoints affected" %(j.get("affected_counter"), j.get("affected_endpoint"))
    return json.dumps(ret)
