# -*- coding:utf-8 -*-
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

