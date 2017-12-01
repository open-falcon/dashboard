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
from rrd.config import API_ADDR
from rrd import corelib

class Endpoint(object):
    def __init__(self, id, endpoint, ts):
        self.id = str(id)
        self.endpoint = endpoint
        self.ts = ts

    def __repr__(self):
        return "<Endpoint id=%s, endpoint=%s>" %(self.id, self.id)
    __str__ = __repr__


    @classmethod
    def gets_by_endpoint(cls, endpoints, deadline=0):
        if not endpoints:
            return []

        h = {"Content-type": "application/json"}
        qs = "deadline=%d" %deadline
        for x in endpoints:
            qs += "&endpoints=%s" %x
        r = corelib.auth_requests("GET", API_ADDR + "/graph/endpointobj?%s" %qs, headers=h)
        if r.status_code != 200:
            raise Exception(r.text)
        j = r.json() or []
        return [cls(*[x["id"], x["endpoint"], x["ts"]]) for x in j]

class EndpointCounter(object):
    def __init__(self, endpoint_id, counter, step, type_):
        self.endpoint_id = str(endpoint_id)
        self.counter = counter
        self.step = step
        self.type_ = type_

    def __repr__(self):
        return "<EndpointCounter endpoint_id=%s, counter=%s>" %(self.endpoint_id, self.counter)
    __str__ = __repr__

    @classmethod
    def search_in_endpoint_ids(cls, qs, endpoint_ids, limit=100):
        if not endpoint_ids:
            return []

        eid_str = ",".join(endpoint_ids)
        r = corelib.auth_requests("GET", API_ADDR + "/graph/endpoint_counter?eid=%s&metricQuery=%s&limit=%d" %(eid_str, " ".join(qs), limit))
        if r.status_code != 200:
            raise Exception(r.text)
        j = r.json() or []

        return [cls(*[x["endpoint_id"], x["counter"], x["step"], x["type"]]) for x in j]
