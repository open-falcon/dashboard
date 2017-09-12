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


class Strategy(Bean):
    _tbl = 'strategy'
    _cols = 'id,metric,tags,max_step,priority,func,op,right_value,note,run_begin,run_end,tpl_id'

    def __init__(self, _id, metric, tags, max_step, priority, func, op, right_value, note, run_begin, run_end, tpl_id):
        self.id = _id
        self.metric = metric
        self.tags = tags
        self.max_step = max_step
        self.priority = priority
        self.func = func
        self.op = op
        self.right_value = right_value
        self.note = note
        self.run_begin = run_begin
        self.run_end = run_end
        self.tpl_id = tpl_id

    def to_json(self):
        return {
            'id': self.id,
            'metric': self.metric,
            'tags': self.tags,
            'max_step': self.max_step,
            'priority': self.priority,
            'func': self.func,
            'op': self.op,
            'right_value': self.right_value,
            'note': self.note,
            'run_begin': self.run_begin,
            'run_end': self.run_end,
            'tpl_id': self.tpl_id
        }

