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
import copy
import re
from rrd import config
from rrd.model.tmpgraph import TmpGraph

def generate_graph_urls(graph, start, end):
    counters = graph.counters or []
    if not counters:
        return []

    endpoint_list = graph.hosts or []
    if not endpoint_list:
        return []

    return _generate_graph_urls(graph, counters, endpoint_list, start, end)

def _generate_graph_urls(graph, counters, endpoint_list, start, end):
    ret_graphs = []

    if graph.graph_type == 'h':
        for c in counters:
            tmp_graph_id = TmpGraph.add(endpoint_list, [c,])
            if not tmp_graph_id:
                break

            new_g = copy.deepcopy(graph)
            new_g.counters = c
            if end:
                new_g.src = '''/chart/h?id=%s&start=%s&end=%s''' %(tmp_graph_id, start or (0-graph.timespan), end)
            else:
                new_g.src = '''/chart/h?id=%s&start=%s''' %(tmp_graph_id, start or (0-graph.timespan))
            if graph.method == 'SUM':
                new_g.src += "&sum=on"
            else:
                new_g.src += "&cf=%s" %graph.method

            ret_graphs.append(new_g)
    elif graph.graph_type=='k':
        for e in endpoint_list:
            tmp_graph_id = TmpGraph.add([e,], counters)
            if not tmp_graph_id:
                break

            new_g = copy.deepcopy(graph)
            new_g.hosts = e
            if end:
                new_g.src = '''/chart/k?id=%s&start=%s&end=%s''' %(tmp_graph_id, start or (0-graph.timespan), end)
            else:
                new_g.src = '''/chart/k?id=%s&start=%s''' %(tmp_graph_id, start or (0-graph.timespan))
            if graph.method == 'SUM':
                new_g.src += "&sum=on"
            else:
                new_g.src += "&cf=%s" %graph.method

            ret_graphs.append(new_g)
    else:
        #组合视角
        tmp_graph_id = TmpGraph.add(endpoint_list, counters)
        if not tmp_graph_id:
            return []
        new_g = copy.deepcopy(graph)
        if end:
            new_g.src = '''/chart/a?id=%s&start=%s&end=%s''' %(tmp_graph_id, start or (0-graph.timespan), end)
        else:
            new_g.src = '''/chart/a?id=%s&start=%s''' %(tmp_graph_id, start or (0-graph.timespan))
        if graph.method == 'SUM':
            new_g.src += "&sum=on"
        else:
            new_g.src += "&cf=%s" %graph.method

        ret_graphs.append(new_g)

    return ret_graphs

