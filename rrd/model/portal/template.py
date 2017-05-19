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
from rrd.config import MAINTAINERS
from .strategy import Strategy
from .action import Action
from rrd.model.user import User


class Template(Bean):
    _tbl = 'tpl'
    _cols = 'id, tpl_name, parent_id, action_id, create_user'

    def __init__(self, _id, tpl_name, parent_id, action_id, create_user):
        self.id = _id
        self.tpl_name = tpl_name
        self.parent_id = parent_id
        self.action_id = action_id
        self.create_user = create_user
        self.parent = None
        self.action = None

    def to_json(self):
        return {
            'id': self.id,
            'name': self.tpl_name,
            'parent_id': self.parent_id,
            'action_id': self.action_id,
            'create_user': self.create_user,
        }

    @classmethod
    def query(cls, page, limit, query, me=None):
        where = ''
        params = []

        if me is not None:
            where = 'create_user = %s'
            params = [me]

        if query:
            where += ' and ' if where else ''
            where += 'tpl_name like %s'
            params.append('%' + query + '%')

        vs = cls.select_vs(where=where, params=params, page=page, limit=limit, order='tpl_name')
        total = cls.total(where, params)
        return vs, total

    def writable(self, login_user):
        #login_user can be str or User obj
        if isinstance(login_user, str):
            login_user = User.get_by_name(login_user)

        if not login_user:
            return False

        if login_user.is_admin() or login_user.is_root():
            return True

        if self.create_user == login_user.name:
            return True

        if login_user.name in MAINTAINERS:
            return True

        a = self.action
        if not a:
            return False

        if not a.uic:
            return False

        return login_user.in_teams(a.uic)

    def fork(self, login_user):
        new_name = 'copy_of_' + self.tpl_name
        if self.__class__.read('tpl_name=%s', [new_name]):
            return -1

        # fork action
        action_id = self.action_id
        if action_id:
            action = Action.get(action_id)
            if action:
                action_id = Action.insert(
                    {
                        'uic': action.uic,
                        'url': action.url,
                        'callback': action.callback,
                        'before_callback_sms': action.before_callback_sms,
                        'before_callback_mail': action.before_callback_mail,
                        'after_callback_sms': action.after_callback_sms,
                        'after_callback_mail': action.after_callback_mail,
                    }
                )

        # fork tpl
        tpl_id = self.__class__.insert({
            'tpl_name': new_name,
            'parent_id': self.parent_id,
            'action_id': action_id,
            'create_user': login_user,
        })

        # fork strategy
        ss = Strategy.select_vs(where='tpl_id = %s', params=[self.id])
        for s in ss:
            Strategy.insert({
                'metric': s.metric,
                'tags': s.tags,
                'max_step': s.max_step,
                'priority': s.priority,
                'func': s.func,
                'op': s.op,
                'right_value': s.right_value,
                'note': s.note,
                'run_begin': s.run_begin,
                'run_end': s.run_end,
                'tpl_id': tpl_id,
            })

        return tpl_id
