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


from rrd.config import API_ADDR
import json
from rrd import corelib

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
    r = corelib.auth_requests("POST", "%s/graph/history" %API_ADDR, headers=h, data=json.dumps(params))
    if r.status_code != 200:
        raise Exception("%s : %s" %(r.status_code, r.text))

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
