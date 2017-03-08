# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'
from .bean import Bean
from rrd.config import MAINTAINERS
import time


class Nodata(Bean):
    _tbl = 'mockcfg'
    _cols = 'id, name, obj, obj_type, metric, tags, dstype, step, mock, creator, t_create, t_modify'
    _max_obj_items = 5
    _max_obj_len = 1024

    def __init__(self, _id, name, obj, obj_type, metric, tags, dstype, step, mock, creator,
                 t_create, t_modify):
        self.id = _id
        self.name = name
        self.obj = obj
        self.obj_type = obj_type
        self.metric = metric
        self.tags = tags
        self.dstype = dstype
        self.step = step
        self.mock = mock
        self.creator = creator
        self.t_create = t_create
        self.t_modify = t_modify
 
    @classmethod
    def query(cls, page, limit, query, me=None):
        where = ''
        params = []

        if me is not None:
            where = 'creator = %s'
            params.append(me)

        if query:
            where += ' and ' if where else ''
            where += ' name like %s'
            params.append('%' + query + '%')

        vs = cls.select_vs(where=where, params=params, page=page, limit=limit)
        total = cls.total(where=where, params=params)
        return vs, total

    @classmethod
    def save_or_update(cls, nodata_id, name, obj, obj_type, metric, tags, dstype, step, mock, login_user):
        if len(obj) > cls._max_obj_len:
            return 'endpoint too long'

        obj_len = len(obj.strip().split('\n'))
        if obj_len > cls._max_obj_items:
            return 'endpoint too many items'

        if nodata_id:
            return cls.update_nodata(nodata_id, name, obj, obj_type, metric, tags, dstype, step, mock)
        else:
            return cls.insert_nodata(name, obj, obj_type, metric, tags, dstype, step, mock, login_user)

    @classmethod
    def insert_nodata(cls, name, obj, obj_type, metric, tags, dstype, step, mock, login_user):
        nodata_id = Nodata.insert({
            'name' : name,
            'obj' : obj,
            'obj_type' : obj_type,
            'metric' : metric,
            'tags' : tags,
            'dstype' : dstype,
            'step' : step,
            'mock': mock,
            'creator': login_user,
            't_create': time.strftime('%Y-%m-%d %H:%M:%S')
        })

        if nodata_id:
            return ''

        return 'save nodata fail'

    @classmethod
    def update_nodata(cls, nodata_id, name, obj, obj_type, metric, tags, dstype, step, mock):
        e = Nodata.get(nodata_id)
        if not e:
            return 'no such nodata config %s' % nodata_id

        Nodata.update_dict(
            {
                'name' : name,
                'obj' : obj,
                'obj_type' : obj_type,
                'metric' : metric,
                'tags' : tags,
                'dstype' : dstype,
                'step' : step,
                'mock': mock,
            },
            'id=%s',
            [e.id]
        )
        return ''

    def writable(self, login_user):
        #login_user can be str or User obj
        if isinstance(login_user, str):
            login_user = User.get_by_name(login_user)

        if not login_user:
            return False

        if login_user.is_admin() or login_user.is_root():
            return True

        if self.creator == login_user.name:
            return True

        if login_user.name in MAINTAINERS:
            return True

        return False
