#-*- coding:utf-8 -*-
import requests
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

