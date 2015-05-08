#-*- coding:utf-8 -*-
import json
from flask import request, abort, g
from rrd import app

from rrd.model.tag_endpoint import TagEndpoint
from rrd.model.endpoint import Endpoint
from rrd.model.endpoint_counter import EndpointCounter
from rrd.model.graph import TmpGraph

@app.route("/api/endpoints")
def api_endpoints():
    ret = {
        "ok": False,
        "msg": "",
        "data": [],
    }

    q = request.args.get("q") or ""
    raw_tag = request.args.get("tags") or ""
    tags = raw_tag and [x.strip() for x in raw_tag.split(",")] or []
    limit = int(request.args.get("limit") or 100)

    if not q and not tags:
        ret["msg"] = "no query params given"
        return json.dumps(ret)
    
    endpoints = []

    if tags and q:
        endpoint_ids = TagEndpoint.get_endpoint_ids(tags, limit=limit) or []
        endpoints = Endpoint.search_in_ids(q.split(), endpoint_ids)
    elif tags:
        endpoint_ids = TagEndpoint.get_endpoint_ids(tags, limit=limit) or []
        endpoints = Endpoint.gets(endpoint_ids)
    else:
        endpoints = Endpoint.search(q.split(), limit=limit)

    endpoints_str = [x.endpoint for x in endpoints]
    endpoints_str.sort()
    ret['data'] = endpoints_str
    ret['ok'] = True

    return json.dumps(ret)


@app.route("/api/counters", methods=["POST"])
def api_get_counters():
    ret = {
        "ok": False,
        "msg": "",
        "data": [],
    }
    endpoints = request.form.get("endpoints") or ""
    endpoints = endpoints and json.loads(endpoints)
    q = request.form.get("q") or ""
    limit = int(request.form.get("limit") or 100)

    if not (endpoints or q):
        ret['msg'] = "no endpoints or counter given"
        return json.dumps(ret)

    endpoint_objs = Endpoint.gets_by_endpoint(endpoints)
    endpoint_ids = [x.id for x in endpoint_objs]
    if not endpoint_ids:
        ret['msg'] = "no endpoints in graph"
        return json.dumps(ret)

    if q:
        qs = q.split()
        ecs = EndpointCounter.search_in_endpoint_ids(qs, endpoint_ids, limit=limit)
    else:
        ecs = EndpointCounter.gets_by_endpoint_ids(endpoint_ids, limit=limit)

    if not ecs:
        ret["msg"] = "no counters in graph"
        return json.dumps(ret)
    
    counters_map = {}
    for x in ecs:
        counters_map[x.counter] = [x.counter, x.type_, x.step]
    sorted_counters = sorted(counters_map.keys())
    sorted_values = [counters_map[x] for x in sorted_counters]

    ret['data'] = sorted_values
    ret['ok'] = True

    return json.dumps(ret)

@app.route("/api/tmpgraph", methods=["POST",])
def api_create_tmpgraph():
    d = request.data
    jdata = json.loads(d)
    endpoints = jdata.get("endpoints") or []
    counters = jdata.get("counters") or []
    id_ = TmpGraph.add(endpoints, counters)

    ret = {
        "ok": False,
        "id": id_,
    }
    if id_:
        ret['ok'] = True
        return json.dumps(ret)
    else:
        return json.dumps(ret)
