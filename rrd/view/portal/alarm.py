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


from flask import jsonify, render_template, request, g, abort
from rrd import app
from rrd.model.portal.alarm import Event, EventCase
import json

@app.route("/portal/alarm-dash/case")
def alarm_dash_case_get():
    event_cases = []
    limit = int(request.args.get("limit") or 10)
    page = int(request.args.get("p") or 1)
    endpoint_q = request.args.get("endpoint_q") or ""
    metric_q = request.args.get("metric_q") or ""
    status = request.args.get("status") or ""

    cases, total = EventCase.query(page, limit, endpoint_q, metric_q, status)
    return render_template("portal/alarm/case.html", **locals())

@app.route("/portal/alarm-dash/case/event")
def alarm_dash_event_get():
    limit = int(request.args.get("limit") or 10)
    page = int(request.args.get("p") or 1)

    case_id = request.args.get("case_id")
    if not case_id:
        abort(400, "no case id")

    _cases = EventCase.select_vs(where='id=%s', params=[case_id], limit=1)
    if len(_cases) == 0:
        abort(400, "no such case where id=%s" %case_id)
    case = _cases[0]

    case_events, total = Event.query(event_caseId=case_id, page=page, limit=limit)
    return render_template("portal/alarm/case_events.html", **locals())


@app.route("/portal/alarm-dash/case/delete", methods=['POST'])
def alarm_dash_case_delete():
    ret = {
        "msg": "",
    }
    ids = request.form.get("ids") or ""
    ids = ids.split(",") or []
    if not ids:
       ret['msg'] = "no case ids" 
       return json.dumps(ret)

    holders = []
    for x in ids:
        holders.append("%s")
    placeholder = ','.join(holders)

    where = 'id in (' + placeholder + ')'
    params = ids
    EventCase.delete(where=where, params=params)
    for x in ids:
        Event.delete(where='event_caseId=%s', params=[x])

    return json.dumps(ret)

@app.route("/portal/alarm-dash/case/event/delete", methods=['POST'])
def alarm_dash_case_event_delete():
    ret = {
        "msg": "",
    }
    ids = request.form.get("ids") or ""
    ids = ids.split(",") or []
    if not ids:
       ret['msg'] = "no case ids" 
       return json.dumps(ret)

    holders = []
    for x in ids:
        holders.append("%s")
    placeholder = ','.join(holders)

    where = 'id in (' + placeholder + ')'
    params = ids
    Event.delete(where=where, params=params)

    return json.dumps(ret)
