#-*- coding:utf-8 -*-
import json
import requests
from rrd.config import API_ADDR

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
        r = requests.get(API_ADDR + "/dashboard/tmpgraph/%s" %(id,))
        if r.status_code != 200:
            return

        j = r.json()
        return j and cls(*[id, j["endpoints"], j["counters"]])


    @classmethod
    def add(cls, endpoints, counters):
        d = {
            "endpoints": endpoints,
            "counters": counters,
        }
        headers = {'Content-type': 'application/json'}
        r = requests.post(API_ADDR + "/dashboard/tmpgraph", headers=headers, data=json.dumps(d))
        if r.status_code != 200:
            return

        j = r.json()
        return j and j.get('id')

'''
CREATE TABLE `tmp_graph` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`endpoints` varchar(10240) NOT NULL DEFAULT '',
`counters` varchar(10240) NOT NULL DEFAULT '',
`ck` varchar(32) NOT NULL,
`time_` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`id`),
UNIQUE KEY `idx_ck` (`ck`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
