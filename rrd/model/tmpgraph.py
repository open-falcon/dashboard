#-*- coding:utf-8 -*-
import json
from rrd.config import API_ADDR
from rrd import corelib

class TmpGraph(object):
    def __init__(self, id, endpoints, counters):
        self.id = str(id)
        self.endpoints = endpoints or []
        self.endpoints = filter(None, [x.strip() for x in self.endpoints])
        self.counters = counters or []
        self.counters = filter(None, [x.strip() for x in self.counters])

    def __repr__(self):
        return "<TmpGraph id=%s, endpoints=%s, counters=%s>" %(self.id, self.endpoints, self.counters)
    __str__ = __repr__

    @classmethod
    def get(cls, id):
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("GET", API_ADDR + "/dashboard/tmpgraph/%s" %(id,), headers=h)
        if r.status_code != 200:
            raise Exception(r.text)

        j = r.json()
        return j and cls(*[id, j["endpoints"], j["counters"]])


    @classmethod
    def add(cls, endpoints, counters):
        d = {
            "endpoints": endpoints,
            "counters": counters,
        }
        h = {'Content-type': 'application/json'}
        r = corelib.auth_requests("POST", API_ADDR + "/dashboard/tmpgraph", headers=h, data=json.dumps(d))
        if r.status_code != 200:
            raise Exception(r.text)

        j = r.json()
        return j and j.get('id')

