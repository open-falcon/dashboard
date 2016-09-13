#-*- coding:utf-8 -*-
from rrd.store import dashboard_db_conn as db_conn

class EndpointAlias(object):
    def __init__(self, id, endpoint, alias):
        self.id = str(id)
        self.endpoint = endpoint
        self.alias = alias


    @classmethod
    def searchAlias(cls):
        sql = '''select id, endpoint, alias from endpoint_alias '''

        cursor = db_conn.execute(sql)
        rows = cursor.fetchall()
        cursor and cursor.close()
        return [cls(*row) for row in rows]