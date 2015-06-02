#-*- coding:utf-8 -*-
import requests
import json
import copy
import re
from rrd import config
from rrd.consts import ENDPOINT_DELIMITER
from rrd.model.graph import TmpGraph
from rrd.model.endpoint import Endpoint
from rrd.model.endpoint_counter import EndpointCounter

def generate_graph_urls(graph, start, end):
    counters = graph.counters or []
    if not counters:
        return []

    endpoint_list = graph.hosts or []
    if not endpoint_list:
        return []

    endpoint_objs = Endpoint.gets_by_endpoint(endpoint_list)
    if not endpoint_objs:
        return []
    endpoint_ids = [x.id for x in endpoint_objs]

    counters = []
    for c in graph.counters:
        if c.find("metric=") == -1:
            counters.append(c)
        else:
            metric=""
            tags = []
            qs = []
            c = c.strip()
            for q in c.split():
                q = q.strip()
                if q.startswith("metric="):
                    metric = q.replace("metric=", "", 1)
                    qs.append(metric)
                else:
                    qs.append(q)
                    tags.append(q)

            counter_objs = EndpointCounter.search_in_endpoint_ids(qs, endpoint_ids[:], limit=100)
            if not counter_objs:
                continue
            for co in counter_objs:
                if not re.search('^%s(/|$)' %metric, co.counter):
                    continue

                matched = True
                for tag in tags:
                    if not re.search('(/|,)%s(,|$)' %tag, co.counter):
                        matched = False
                        break
                if not matched:
                    continue

                counters.append(co.counter)

    if not counters:
        return []
    counters = sorted(list(set(counters)))

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
            tmp_graph_id = create_tmp_graph([e,], counters)
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
        tmp_graph_id = create_tmp_graph(endpoint_list, counters)
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

def create_tmp_graph(endpoints, counters):
    id_ = TmpGraph.add(endpoints, counters)
    return id_

