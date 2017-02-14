#-*- coding:utf-8 -*-
import requests
from rrd.config import API_ADDR
import json

def graph_history(endpoints, counters, cf, start, end):
    #TODO:step
    params = {
        "start_time": start,
        "end_time": end,
        "consol_fun": cf,
        "hostnames": endpoints,
        "counters": counters,
    }
    h = {"Content-type": "application/json"}
    r = requests.post("%s/graph/history" %API_ADDR, headers=h, data=json.dumps(params))
    if r.status_code != 200:
        raise Exception("{} : {}".format(r.status_code, r.text))

    return r.json()

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
