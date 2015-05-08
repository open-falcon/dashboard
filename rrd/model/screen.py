#-*- coding:utf-8 -*-
from rrd.store import dashboard_db_conn as db_conn

class DashboardScreen(object):
    def __init__(self, id, pid, name, time):
        self.id = str(id)
        self.pid = str(pid)
        self.name = name
        self.time = time

    def __repr__(self):
        return "<DashboardScreen id=%s, name=%s, pid=%s>" %(self.id, self.name, self.pid)
    __str__ = __repr__

    @classmethod
    def get(cls, id):
        cursor = db_conn.execute('''select id, pid, name, time from dashboard_screen where id=%s''', (id,))
        row = cursor.fetchone()
        cursor.close()
        return row and cls(*row)

    @classmethod
    def gets(cls, pid=None, start=0, limit=0):
        assert limit >= 0
        if pid is not None:
            if limit > 0:
                cursor = db_conn.execute('''select id, pid, name, time from dashboard_screen where pid=%s limit %s, %s''', (pid, start, limit))
            else:
                cursor = db_conn.execute('''select id, pid, name, time from dashboard_screen where pid=%s''', (pid,))
        else:
            if limit > 0:
                cursor = db_conn.execute('''select id, pid, name, time from dashboard_screen limit %s, %s''', (start, limit))
            else:
                cursor = db_conn.execute('''select id, pid, name, time from dashboard_screen''')
        rows = cursor.fetchall()
        cursor.close()
        return [cls(*row) for row in rows]

    @classmethod
    def add(cls, pid, name):
        cursor = db_conn.execute('''insert into dashboard_screen (pid, name) values(%s, %s)''', (pid, name))
        id_ = cursor.lastrowid
        db_conn.commit()
        cursor.close()
        return cls.get(id_)

    @classmethod
    def remove(cls, id):
        db_conn.execute('''delete from dashboard_screen where id=%s''', (id,))
        db_conn.commit()

    def update(self, pid=None, name=None):
        pid = pid or self.pid
        name = name or self.name
        db_conn.execute('''update dashboard_screen set pid=%s, name=%s where id=%s''', (pid, name, self.id))
        db_conn.commit()
        return DashboardScreen.get(self.id)
