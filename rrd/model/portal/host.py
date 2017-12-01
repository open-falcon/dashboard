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
from rrd.store import db

class Host(Bean):
    _tbl = 'host'
    _cols = 'id, hostname, maintain_begin, maintain_end'

    def __init__(self, _id, hostname, maintain_begin, maintain_end):
        self.id = _id
        self.hostname = hostname
        self.maintain_begin = maintain_begin
        self.maintain_end = maintain_end

    @classmethod
    def query(cls, page, limit, query, maintaining, group_id):
        where = 'id in (select host_id from grp_host where grp_id = %s)'
        params = [group_id]

        if maintaining == '1':
            where += ' and maintain_begin > 0 and maintain_end > 0'

        if query:
            where += ' and hostname like %s'
            params.append('%' + query + '%')

        vs = cls.select_vs(where=where, params=params, page=page, limit=limit, order='hostname')
        total = cls.total(where, params)
        return vs, total

    @classmethod
    def maintain(cls, begin, end, host_ids):
        if not host_ids:
            return 'host ids is blank'

        cls.update('maintain_begin = %s, maintain_end = %s where id in (%s)' % (begin, end, host_ids))
        return ''

    @classmethod
    def no_maintain(cls, host_ids):
        if not host_ids:
            return 'host ids is blank'
        cls.update('maintain_begin = 0, maintain_end = 0 where id in (%s)' % host_ids)
        return ''

    @classmethod
    def all_host_dict(cls):
        rows = db.query_all('SELECT id, hostname FROM host')
        ret = {}
        if rows:
            for row in rows:
                ret[row[0]] = row[1]
        return ret

    @classmethod
    def add(cls, host_id, hostname):
        if cls.exists('id=%s', [host_id]):
            return
        cls.insert({'id': host_id, 'hostname': hostname})

    @classmethod
    def create(cls, hostname):
        if cls.exists('hostname=%s', [hostname]):
            return
        cls.insert({'hostname': hostname})
