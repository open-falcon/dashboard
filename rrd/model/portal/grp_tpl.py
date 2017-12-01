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
from .template import Template
from .host_group import HostGroup


class GrpTpl(Bean):
    _tbl = 'grp_tpl'
    _cols = 'grp_id, tpl_id, bind_user'
    _id = ''

    def __init__(self, grp_id, tpl_id, bind_user):
        self.grp_id = grp_id
        self.tpl_id = tpl_id
        self.bind_user = bind_user

    @classmethod
    def tpl_list(cls, grp_id=None):
        if not grp_id:
            return []

        tpl_ids = cls.column('tpl_id', where='grp_id=%s', params=[grp_id])
        if not tpl_ids:
            return []

        tpl_ids = ['%s' % i for i in tpl_ids]
        ids = ','.join(tpl_ids)
        return Template.select_vs(where='id in (%s)' % ids)

    @classmethod
    def tpl_set(cls, group_ids=None):
        if group_ids is None:
            group_ids = []

        if not group_ids:
            return []

        grp_ids = ['%s' % i for i in group_ids]
        tpl_ids = cls.column('tpl_id', where='grp_id in (%s)' % ', '.join(grp_ids))
        if not tpl_ids:
            return []

        tpl_ids = ['%s' % i for i in tpl_ids]
        ids = ','.join(tpl_ids)
        return Template.select_vs(where='id in (%s)' % ids)

    @classmethod
    def grp_list(cls, tpl_id=None):
        if not tpl_id:
            return []

        grp_ids = cls.column('grp_id', where='tpl_id=%s', params=[tpl_id])
        if not grp_ids:
            return []

        grp_ids = ['%s' % i for i in grp_ids]
        ids = ','.join(grp_ids)
        return HostGroup.select_vs(where='id in (%s)' % ids)

    @classmethod
    def unbind(cls, grp_id, tpl_id):
        return cls.delete('grp_id = %s and tpl_id = %s', [grp_id, tpl_id])

    @classmethod
    def bind(cls, grp_id, tpl_id, login_user):
        if cls.exists('grp_id=%s and tpl_id=%s', [grp_id, tpl_id]):
            return

        cls.insert({
            'grp_id': grp_id,
            'tpl_id': tpl_id,
            'bind_user': login_user,
        })

    @classmethod
    def unbind_tpl(cls, tpl_id):
        return cls.delete('tpl_id=%s', [tpl_id])

    @classmethod
    def unbind_group(cls, grp_id):
        return cls.delete('grp_id=%s', [grp_id])
