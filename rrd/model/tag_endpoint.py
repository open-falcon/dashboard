#-*- coding:utf-8 -*-
from rrd.store import graph_db_conn as db_conn

class TagEndpoint(object):
    def __init__(self, id, tag, endpoint_id):
        self.id = str(id)
        self.tag = tag
        self.endpoint_id = str(endpoint_id)


    @classmethod
    def get_endpoint_ids(cls, tags, limit=200):
        if not tags:
            return []

        holders = ["%s" for x in tags]
        placeholder = ",".join(holders)
        args = tags
        cursor = db_conn.execute('''select distinct endpoint_id from tag_endpoint where tag in (''' + placeholder + ''')''', args)
        rows = cursor.fetchall()
        ids = [x[0] for x in rows]

        if not ids:
            return []

        res = None
        for t in tags:
            holders = ["%s" for x in ids]
            placeholder = ",".join(holders)
            args = list(ids) + [t, ]
            sql = '''select endpoint_id from tag_endpoint where endpoint_id in (''' + placeholder + ''') and tag=%s'''
            cursor = db_conn.execute(sql, args)
            rows = cursor.fetchall()
            cursor and cursor.close()

            if not rows:
                return []

            if res is None:
                res = set([row[0] for row in rows])
            else:
                res.intersection_update(set([row[0] for row in rows]))

        ret = list(res) if res else []
        return ret[:limit]


