# -*- coding:utf-8 -*-
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
