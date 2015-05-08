#-*- coding:utf-8 -*-
from rrd.store import graph_db_conn as db_conn

class Endpoint(object):
    def __init__(self, id, endpoint, ts):
        self.id = str(id)
        self.endpoint = endpoint
        self.ts = ts

    def __repr__(self):
        return "<Endpoint id=%s, endpoint=%s>" %(self.id, self.id)
    __str__ = __repr__

    @classmethod
    def search(cls, qs, start=0, limit=100, deadline=0):
        args = [deadline, ]
        for q in qs:
            args.append("%"+q+"%")
        args += [start, limit]

        sql = '''select id, endpoint, ts from endpoint where ts > %s '''
        for q in qs:
            sql += ''' and endpoint like %s'''
        sql += ''' limit %s,%s'''

        cursor = db_conn.execute(sql, args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

    @classmethod
    def search_in_ids(cls, qs, ids, deadline=0):
        if not ids:
            return []

        holders = ["%s" for x in ids]
        placeholder = ",".join(holders)

        args = ids + [deadline, ]
        for q in qs:
            args.append("%"+q+"%")

        sql = '''select id, endpoint, ts from endpoint where id in (''' + placeholder + ''') and ts > %s '''
        for q in qs:
            sql += ''' and endpoint like %s'''

        cursor = db_conn.execute(sql, args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

    @classmethod
    def gets_by_endpoint(cls, endpoints, deadline=0):
        if not endpoints:
            return []

        holders = ["%s" for x in endpoints]
        placeholder = ",".join(holders)
        args = endpoints + [deadline, ]

        cursor = db_conn.execute('''select id, endpoint, ts from endpoint where endpoint in (''' + placeholder + ''') and ts > %s''', args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

    @classmethod
    def gets(cls, ids, deadline=0):
        if not ids:
            return []

        holders = ["%s" for x in ids]
        placeholder = ",".join(holders)
        args = ids + [deadline, ]

        cursor = db_conn.execute('''select id, endpoint, ts from endpoint where id in (''' + placeholder + ''') and ts > %s''', args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]
