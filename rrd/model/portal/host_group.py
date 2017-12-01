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
from rrd.store import db
from rrd.model.user import User

class HostGroup(Bean):
    _tbl = 'grp'
    _cols = 'id, grp_name, create_user, come_from'
    _id = 'id'

    def __init__(self, _id, grp_name, create_user, come_from):
        self.id = _id
        self.grp_name = grp_name
        self.create_user = create_user
        self.come_from = come_from

    #TODO:admin should manage the group
    def writable(self, user):
        #user can be str or User obj
        if isinstance(user, str):
            user = User.get_by_name(user)

        if not user:
            return False

        if self.create_user == user.name or user.name in MAINTAINERS or user.is_admin() or user.is_root():
            return True

        return False

    @classmethod
    def query(cls, page, limit, query, me=None):
        where = ''
        params = []

        if me is not None:
            where = 'create_user = %s'
            params = [me]

        if query:
            where += ' and ' if where else ''
            where += 'grp_name like %s'
            params.append('%' + query + '%')

        vs = cls.select_vs(where=where, params=params, page=page, limit=limit, order='grp_name')
        total = cls.total(where, params)
        return vs, total

    @classmethod
    def create(cls, grp_name, user_name, come_from):
        # check duplicate grp_name
        if cls.column('id', where='grp_name = %s', params=[grp_name]):
            return -1

        return cls.insert({'grp_name': grp_name, 'create_user': user_name, 'come_from': come_from})

    @classmethod
    def all_group_dict(cls):
        rows = db.query_all('select id, grp_name from grp where come_from = 0')
        return [{'id': row[0], 'name': row[1]} for row in rows]

    @classmethod
    def all_set(cls):
        sql = 'select id, grp_name from %s' % cls._tbl
        rows = db.query_all(sql)
        name_set = dict()
        name_id = dict()
        for row in rows:
            name = row[1]
            name_set[name] = set(name.split('_'))
            name_id[name] = row[0]
        return name_set, name_id
