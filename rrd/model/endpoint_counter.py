#-*- coding:utf-8 -*-
from rrd.store import graph_db_conn as db_conn

class EndpointCounter(object):
    def __init__(self, id, endpoint_id, counter, step, type_):
        self.id = str(id)
        self.endpoint_id = str(endpoint_id)
        self.counter = counter
        self.step = step
        self.type_ = type_

    def __repr__(self):
        return "<EndpointCounter id=%s, endpoint_id=%s, counter=%s>" %(self.id, self.endpoint_id, self.counter)
    __str__ = __repr__

    @classmethod
    def search_in_endpoint_ids(cls, qs, endpoint_ids, start=0, limit=100):
        if not endpoint_ids:
            return []

        holders = ["%s" for x in endpoint_ids]
        placeholder = ",".join(holders)

        args = endpoint_ids
        for q in qs:
            args.append("%"+q+"%")
        args += [start, limit]

        sql = '''select id, endpoint_id, counter, step, type from endpoint_counter where endpoint_id in (''' +placeholder+ ''') '''
        for q in qs:
            sql += ''' and counter like %s'''
        sql += ''' limit %s,%s'''

        cursor = db_conn.execute(sql, args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

    @classmethod
    def gets_by_endpoint_ids(cls, endpoint_ids, start=0, limit=100):
        if not endpoint_ids:
            return []

        holders = ["%s" for x in endpoint_ids]
        placeholder = ",".join(holders)
        args = endpoint_ids + [start, limit]

        cursor = db_conn.execute('''select id, endpoint_id, counter, step, type from endpoint_counter where endpoint_id in ('''+placeholder+''') limit %s, %s''', args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

    @classmethod
    def gets(cls, ids, deadline=0):
        if not ids:
            return []

        holders = ["%s" for x in ids]
        placeholder = ",".join(holders)
        args = ids + [start, limit]

        cursor = db_conn.execute('''select id, endpoint, ts from endpoint where id in ('''+placeholder+''') and ts > %s''', args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]
