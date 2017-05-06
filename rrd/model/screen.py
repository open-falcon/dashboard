#-*- coding:utf-8 -*-
import json
from rrd.config import API_ADDR
from rrd import corelib

class DashboardScreen(object):
    def __init__(self, id, pid, name):
        self.id = str(id)
        self.pid = str(pid)
        self.name = name

    def __repr__(self):
        return "<DashboardScreen id=%s, name=%s, pid=%s>" %(self.id, self.name, self.pid)
    __str__ = __repr__

    @classmethod
    def get(cls, id):
        r = corelib.auth_requests("GET", API_ADDR + "/dashboard/screen/%s" %(id,))
        if r.status_code != 200:
            raise Exception(r.text)
        j = r.json()
        if j:
            row = [j["id"], j["pid"], j["name"]]
            return cls(*row)

    @classmethod
    def gets_by_pid(cls, pid):
        r = corelib.auth_requests("GET", API_ADDR + "/dashboard/screens/pid/%s" %(pid,))
        if r.status_code != 200:
            raise Exception(r.text)
        j = r.json() or []
        return [cls(*[x["id"], x["pid"], x["name"]]) for x in j]

    @classmethod
    def gets_all(cls, limit=500):
        r = corelib.auth_requests("GET", API_ADDR + "/dashboard/screens?limit=%s" %(limit,))
        if r.status_code != 200:
            raise Exception(r.text)
        j = r.json() or []
        return [cls(*[x["id"], x["pid"], x["name"]]) for x in j]

    @classmethod
    def add(cls, pid, name):
        d = {"pid": pid, "name": name}
        r = corelib.auth_requests("POST", API_ADDR + "/dashboard/screen", data = d)
        if r.status_code != 200:
            raise Exception(r.text)
        j = r.json()
        return cls(*[j["id"], j["pid"], j["name"]])

    @classmethod
    def remove(cls, id):
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("DELETE", API_ADDR + "/dashboard/screen/%s" %(id,), headers=h)
        if r.status_code != 200:
            raise Exception(r.text)
        return r.json()

    def update(self, pid=None, name=None):
        d = {}
        if pid:
            d["pid"] = pid
        if name:
            d["name"] = name

        r = corelib.auth_requests("PUT", API_ADDR + "/dashboard/screen/%s" %self.id, data = d)
        if r.status_code != 200:
            raise Exception(r.text)
        return r.json()
