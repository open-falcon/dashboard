#-*- coding:utf-8 -*-
import json
import re
from flask import request, abort, g
from rrd import app, config
from rrd import corelib

@app.route("/api/endpoints")
def api_endpoints():
    ret = {
            "ok": False,
            "msg": "",
            "data": [],
            }

    q = request.args.get("q") or ""
    raw_tag = request.args.get("tags") or ""
    tags = ','.join(re.split('\s*,\s*', raw_tag))
    limit = int(request.args.get("limit") or 100)

    if not q:
        q = "."
    if not q and not tags:
        ret["msg"] = "no query params given"
        return json.dumps(ret)

    h = {"Content-type": "application/json"}
    r = corelib.auth_requests("GET", config.API_ADDR + "/graph/endpoint?q=%s&limit=%d&tags=%s" %(q, limit, tags), headers=h)
    if r.status_code != 200:
        abort(400, r.text)

    j = sorted(r.json(), key=lambda x:x["endpoint"])
    endpoints = [x["endpoint"] for x in j]

    ret['data'] = j
    ret['ok'] = True

    return json.dumps(ret)

@app.route("/api/counters", methods=["POST"])
def api_get_counters():
    ret = {
            "ok": False,
            "msg": "",
            "data": [],
            }

    q = request.form.get("q") or ""
    limit = int(request.form.get("limit") or 100)
    eids = request.form.get("eids") or ""
    eids = eids and json.loads(eids) or []

    if not (eids or q):
        ret['msg'] = "no endpoints or counter given"
        return json.dumps(ret)


    h = {"Content-type": "application/json"}
    r = corelib.auth_requests("GET", config.API_ADDR + "/graph/endpoint_counter?eid=%s&metricQuery=%s&limit=%s" %(",".join(eids), q, limit), headers=h)
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
