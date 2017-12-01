# -*- coding:utf-8 -*-
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
