#-*- coding:utf-8 -*-
import hashlib
import json
import dateutil.parser
import time

import requests
from rrd.config import QUERY_ADDR

def graph_info(endpoint_counter):
    '''
    params:
        [
                {
                    "endpoint": "xx",
                    "counter": "load.1min",
                },
                {
                    "endpoint": "yy",
                    "counter": "cpu.idle",
                },
        ]

    return:
        [
            {
                "Filename": "/home/work/data/6070/79/794a6adefed6b10550b4aaaf4c10d20c_GAUGE_60.rrd",
                "addr": "graph1:6070",
                "consolFuc": "GAUGE",
                "counter": "load.1min",
                "endpoint": "xx",
                "step": 60
            },
            {
                "Filename": "/home/work/data/6070/3c/3cb8b78377824b867c6324463ac736b6_GAUGE_60.rrd",
                "addr": "graph2:6070",
                "consolFuc": "GAUGE",
                "counter": "cpu.idle",
                "endpoint": "yy",
                "step": 60
            }
        ]
    '''

    if not endpoint_counter:
        return

    r = requests.post("%s/graph/info" %QUERY_ADDR, data=json.dumps(endpoint_counter))
    if r.status_code != 200:
        raise

    return r.json()

def graph_query(endpoint_counters, cf, start, end):
    '''
    params:
        endpoint_counters: [
            {
                "endpoint": "xx",
                "counter": "load.1min",
            },
            {
                "endpoint": "yy",
                "counter": "cpu.idle",
            },
        ]

    return:
        [
            {
                "endpoint": "xx",
                "counter": "yy",
                "Values": [
                    {
                        "timestamp": 1422868140,
                        "value": 0.32183299999999998
                    },
                    {
                        "timestamp": 1422868200,
                        "value": 0.406167
                    },
                ]
            },
            {
                "endpoint": "xx",
                "counter": "yy",
                "Values": [
                    {
                        "timestamp": 1422868140,
                        "value": 0.32183299999999998
                    },
                    {
                        "timestamp": 1422868200,
                        "value": 0.406167
                    },
                ]
            },
        ]

    '''
    params = {
            "start": start,
            "end": end,
            "cf": cf,
            "endpoint_counters": endpoint_counters,
    }
    r = requests.post("%s/graph/history" %QUERY_ADDR, data=json.dumps(params))
    if r.status_code != 200:
        raise Exception("{} : {}".format(r.status_code, r.text))

    return r.json()

def digest_key(endpoint, key):
    s = "%s/%s" %(endpoint.encode("utf8"), key.encode("utf8"))
    return hashlib.md5(s).hexdigest()[:16]

def merge_list(a, b):
    sum = []
    a_len = len(a)
    b_len = len(b)
    l1 = min(a_len, b_len)
    l2 = max(a_len, b_len)

    if a_len < b_len:
        a, b = b, a

    for i in range(0, l1):
        if a[i] is None and b[i] is None:
            sum.append(None)
        elif a[i] is None:
            sum.append(b[i])
        elif b[i] is None:
            sum.append(a[i])
        else:
            sum.append(a[i] + b[i])

    for i in range(l1, l2):
        sum.append(a[i])

    return sum

def CF(cf, values):
    if cf == 'AVERAGE':
        return float(sum(values))/len(values)
    elif cf == 'MAX':
        return max(values)
    elif cf == 'MIN':
        return min(values)
    elif cf == 'LAST':
        return values[-1]

