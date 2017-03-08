# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'
from .bean import Bean


class Cluster(Bean):
    _tbl = 'cluster'
    _cols = 'id, grp_id, numerator, denominator, endpoint, metric, tags, ds_type, step, creator'

    def __init__(self, _id, grp_id, numerator, denominator, endpoint, metric, tags, ds_type, step, creator):
        self.id = _id
        self.grp_id = grp_id
        self.numerator = numerator
        self.denominator = denominator
        self.endpoint = endpoint
        self.metric = metric
        self.tags = tags
        self.ds_type = ds_type
        self.step = step
        self.creator = creator
