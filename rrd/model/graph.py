#-*- coding:utf-8 -*-
import hashlib
import datetime
from rrd.store import dashboard_db_conn as db_conn
from rrd.store import graph_db_conn
from rrd.consts import ENDPOINT_DELIMITER, COUNTER_DELIMITER

class DashboardGraph(object):
    def __init__(self, id, title, hosts, counters, screen_id,
                timespan=3600, graph_type='h', method='', position=0):
        self.id = str(id)
        self.title = title
        self.hosts = hosts or []
        self.counters = counters or []
        self.screen_id = str(screen_id)

        self.timespan = timespan
        self.graph_type = graph_type
        self.method = method.upper()  # method can be ["", "sum", "average", "max", "min", "last"]
        self.position = position or self.id # init as self.id

    def __repr__(self):
        return "<DashboardGraph id=%s, title=%s, screen_id=%s>" %(self.id, self.title, self.screen_id)
    __str__ = __repr__

    @classmethod
    def gets_by_screen_id(cls, screen_id):
        cursor = db_conn.execute('''select id, title, hosts, counters, screen_id,
                timespan, graph_type, method, position 
                from dashboard_graph where screen_id=%s order by position''', (screen_id,))
        rows = cursor.fetchall()
        cursor and cursor.close()
        ret = []
        for row in rows:
            args = list(row)
            args[2] = args[2].split(ENDPOINT_DELIMITER) or []
            args[3] = args[3].split(ENDPOINT_DELIMITER) or []
            ret.append(cls(*args))
        return ret

    @classmethod
    def get(cls, id):
        cursor = db_conn.execute('''select id, title, hosts, counters, screen_id,
                timespan, graph_type, method, position
                from dashboard_graph where id=%s''', (id,))
        row = cursor.fetchone()
        cursor and cursor.close()
        if row:
            args = list(row)
            args[2] = args[2].split(ENDPOINT_DELIMITER) or []
            args[3] = args[3].split(ENDPOINT_DELIMITER) or []
            return cls(*args)

    @classmethod
    def add(cls, title, hosts, counters, screen_id,
                timespan=3600, graph_type='h', method='', position=0):
        cursor = db_conn.execute('''insert into dashboard_graph (title, hosts, counters, screen_id,
                timespan, graph_type, method, position)
                values(%s, %s, %s, %s, %s, %s, %s, %s)''',
                (title, ENDPOINT_DELIMITER.join(hosts) or "", ENDPOINT_DELIMITER.join(counters) or "", screen_id,
                    timespan, graph_type, method, position))
        id_ = cursor.lastrowid
        db_conn.execute('''update dashboard_graph set position=%s where id=%s''', (id_, id_))
        db_conn.commit()
        cursor and cursor.close()
        return cls.get(id_)

    @classmethod
    def remove(cls, id):
        db_conn.execute('''delete from dashboard_graph where id=%s''', (id,))
        db_conn.commit()

    def update(self, title=None, hosts=None, counters=None, screen_id=None,
            timespan=None, graph_type=None, method=None, position=None):

        title = self.title if title is None else title
        hosts = self.hosts if hosts is None else hosts
        hosts = hosts and ENDPOINT_DELIMITER.join(hosts) or ""

        counters = self.counters if counters is None else counters
        counters = counters and ENDPOINT_DELIMITER.join(counters) or ""

        screen_id = screen_id or self.screen_id
        timespan = timespan or self.timespan
        graph_type = graph_type or self.graph_type
        method = method if method is not None else self.method
        position = position or self.position
        db_conn.execute('''update dashboard_graph set title=%s, hosts=%s, counters=%s, screen_id=%s,
                    timespan=%s, graph_type=%s, method=%s, position=%s where id=%s''',
                    (title, hosts, counters, screen_id, timespan, graph_type, method, position, self.id))
        db_conn.commit()
        return DashboardGraph.get(self.id)
    
    @classmethod
    def update_multi(cls, rows):
        for x in rows:
            id = x["id"]
            hosts = x["hosts"] or []
            counters = x["counters"] or []
            db_conn.execute('''update dashboard_graph set hosts=%s, counters=%s where id=%s''',
                    (ENDPOINT_DELIMITER.join(hosts) or "", ENDPOINT_DELIMITER.join(counters) or "", id))
        db_conn.commit()
        


'''
CREATE TABLE `dashboard_graph` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` char(128) NOT NULL,
  `hosts` varchar(10240) NOT NULL DEFAULT '',
  `counters` varchar(1024) NOT NULL DEFAULT '',
  `screen_id` int(11) unsigned NOT NULL,
  `timespan` int(11) unsigned NOT NULL DEFAULT '3600',
  `graph_type` char(2) NOT NULL DEFAULT 'h',
  `method` char(8) DEFAULT '',
  `position` int(11) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_sid` (`screen_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
'''

class TmpGraph(object):
    def __init__(self, id, endpoints, counters, time_):
        self.id = str(id)
        self.endpoints = endpoints or []
        self.endpoints = filter(None, [x.strip() for x in self.endpoints])
        self.counters = counters or []
        self.counters = filter(None, [x.strip() for x in self.counters])
        self.time_ = time_

    def __repr__(self):
        return "<TmpGraph id=%s, endpoints=%s, counters=%s>" %(self.id, self.endpoints, self.counters)
    __str__ = __repr__

    @classmethod
    def get(cls, id):
        cursor = db_conn.execute('''select id, endpoints, counters, time_ from tmp_graph where id=%s''', (id,))
        row = cursor.fetchone()
        cursor and cursor.close()
        if row:
            id, endpoints, counters, time_ = row
            endpoint_list = endpoints and endpoints.split(ENDPOINT_DELIMITER) or []
            counter_list = counters and counters.split(ENDPOINT_DELIMITER) or []
            return cls(id, endpoint_list, counter_list, time_)
        else:
            return None


    @classmethod
    def add(cls, endpoints, counters):
        es = endpoints and ENDPOINT_DELIMITER.join(sorted(endpoints)) or ""
        cs = counters and COUNTER_DELIMITER.join(sorted(counters)) or ""
        ck = hashlib.md5("%s:%s" %(es.encode("utf8"), cs.encode("utf8"))).hexdigest()
        cursor = db_conn.execute('''insert ignore into tmp_graph (endpoints, counters, ck) values(%s, %s, %s) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id),time_=%s''',
                (es, cs, ck, datetime.datetime.now()))
        id_ = cursor.lastrowid
        db_conn.commit()
        cursor and cursor.close()
        return id_

'''
CREATE TABLE `tmp_graph` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`endpoints` varchar(10240) NOT NULL DEFAULT '',
`counters` varchar(10240) NOT NULL DEFAULT '',
`ck` varchar(32) NOT NULL,
`time_` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`id`),
UNIQUE KEY `idx_ck` (`ck`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
