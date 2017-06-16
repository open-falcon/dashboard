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
from .host import Host


class GroupHost(Bean):
    _tbl = 'grp_host'
    _cols = 'grp_id, host_id'

    def __init__(self, grp_id, host_id):
        self.grp_id = grp_id
        self.host_id = host_id

    @classmethod
    def unbind(cls, grp_id, host_ids):
        return cls.delete('grp_id = %s and host_id in (%s)' % (grp_id, host_ids))

    @classmethod
    def bind(cls, group_id, hostname):
        h = Host.read('hostname = %s', [hostname])
        if not h:
            Host.create(hostname)
            h = Host.read('hostname = %s', [hostname])
            if not h:
                return 'host auto add failed'

        if cls.exists('grp_id = %s and host_id = %s', [group_id, h.id]):
            return 'already existent'

        if db.update('insert into grp_host(grp_id, host_id) values(%s, %s)', [group_id, h.id]) <= 0:
            return 'failure'

        return ''

    @classmethod
    def bind_host_id(cls, group_id, host_id):
        if not Host.get(host_id):
            return 'no such host_id'

        if cls.exists('grp_id = %s and host_id = %s', [group_id, host_id]):
            return 'already existent'

        if db.update('insert into grp_host(grp_id, host_id) values(%s, %s)', [group_id, host_id]) <= 0:
            return 'failure'

        return ''

    @classmethod
    def group_ids(cls, host_id):
        return cls.column('grp_id', where='host_id = %s', params=[host_id])
