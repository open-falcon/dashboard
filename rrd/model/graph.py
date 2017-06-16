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

class DashboardGraph(object):
    def __init__(self, id, title, hosts, counters, screen_id,
                timespan=3600, graph_type='h', method='', position=0):
        self.id = str(id)
        self.title = title
        self.hosts = hosts or []
        self.counters = counters or []
        self.screen_id = str(screen_id)

        self.timespan = timespan
        self.graph_type = graph_type
        self.method = method.upper()  # method can be ["", "sum", "average", "max", "min", "last"]
        self.position = position or self.id # init as self.id

    def __repr__(self):
        return "<DashboardGraph id=%s, title=%s, screen_id=%s>" %(self.id, self.title, self.screen_id)
    __str__ = __repr__

    @classmethod
    def gets_by_screen_id(cls, screen_id):
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("GET", API_ADDR + "/dashboard/graphs/screen/%s" %(screen_id,), headers=h)
        if r.status_code != 200:
            raise Exception(r.text)
        j = r.json()
        return [cls(*[x["graph_id"], x["title"], x["endpoints"], x["counters"], \
                x["screen_id"], x["timespan"], x["graph_type"], x["method"], x["position"]]) for x in j]

    @classmethod
    def get(cls, id):
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("GET", API_ADDR + "/dashboard/graph/%s" %(id,), headers=h)
        if r.status_code != 200:
            raise Exception(r.text)
        x = r.json()
        return x and cls(*[x["graph_id"], x["title"], x["endpoints"], x["counters"], \
                x["screen_id"], x["timespan"], x["graph_type"], x["method"], x["position"]])

    @classmethod
    def add(cls, title, hosts, counters, screen_id,
                timespan=3600, graph_type='h', method='', position=0):

        d = {
            "screen_id": int(screen_id),
            "title": title,
            "endpoints": hosts,
            "counters": counters,
            "timespan": int(timespan),
            "graph_type": graph_type,
            "method": method,
            "position": int(position),
            "falcon_tags": "",
        }
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("POST", API_ADDR + "/dashboard/graph", data = json.dumps(d), headers =h )
        if r.status_code != 200:
            raise Exception(r.text)
        j = r.json()

        graph_id = j and j.get("id")
        return graph_id and cls.get(graph_id)

    @classmethod
    def remove(cls, id):
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("DELETE", API_ADDR + "/dashboard/graph/%s" %(id,), headers=h)
        if r.status_code != 200:
            raise Exception(r.text)
        return r.json()

    def update(self, title=None, hosts=None, counters=None, screen_id=None,
            timespan=None, graph_type=None, method=None, position=None):

        title = self.title if title is None else title
        hosts = self.hosts if hosts is None else hosts
        counters = self.counters if counters is None else counters
        screen_id = screen_id or self.screen_id
        timespan = timespan or self.timespan
        graph_type = graph_type or self.graph_type
        method = method if method is not None else self.method
        position = position or self.position
    
        d = {
            "screen_id": int(screen_id),
            "title": title,
            "endpoints": hosts,
            "counters": counters,
            "timespan": int(timespan),
            "graph_type": graph_type,
            "method": method,
            "position": int(position),
            "falcon_tags": "",
        }
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("PUT", API_ADDR + "/dashboard/graph/%s" %(self.id,), data = json.dumps(d), headers =h )
        if r.status_code != 200:
            raise Exception(r.text)
        j = r.json()

        graph_id = j and j.get("id")
        return graph_id and DashboardGraph.get(graph_id)

    @classmethod
    def update_multi(cls, rows):
        for x in rows:
            id = x["id"]
            hosts = x["hosts"] or []
            counters = x["counters"] or []
            grh = cls.get(id)
            grh and grh.update(hosts=hosts, counters=counters)
        
