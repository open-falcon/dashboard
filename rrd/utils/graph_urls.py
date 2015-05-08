#-*- coding:utf-8 -*-
import requests
import json
import copy
from rrd import config
from rrd.consts import ENDPOINT_DELIMITER
from rrd.model.graph import TmpGraph

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
            tmp_graph_id = create_tmp_graph(endpoint_list, [c,])
            if not tmp_graph_id:
                break

            new_g = copy.deepcopy(graph)
            new_g.counters = c
            new_g.src = '''/chart/h?id=%s&start=%s''' %(tmp_graph_id, start or (0-graph.timespan))
            if graph.method == 'SUM':
                new_g.src += "&sum=on"
            else:
                new_g.src += "&cf=%s" %graph.method

            ret_graphs.append(new_g)
    else:
        for e in endpoint_list:
            tmp_graph_id = create_tmp_graph([e,], counters)
            if not tmp_graph_id:
                break

            new_g = copy.deepcopy(graph)
            new_g.hosts = e
            new_g.src = '''/chart/k?id=%s&start=%s''' %(tmp_graph_id, start or (0-graph.timespan))
            if graph.method == 'SUM':
                new_g.src += "&sum=on"
            else:
                new_g.src += "&cf=%s" %graph.method

            ret_graphs.append(new_g)

    return ret_graphs

def create_tmp_graph(endpoints, counters):
    id_ = TmpGraph.add(endpoints, counters)
    return id_

