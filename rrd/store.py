#-*- coding:utf-8 -*-
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


import MySQLdb
from rrd import config
from rrd.utils.logger import logging

portal_db_cfg = {
        "DB_HOST": config.PORTAL_DB_HOST,
        "DB_PORT": config.PORTAL_DB_PORT,
        "DB_USER": config.PORTAL_DB_USER,
        "DB_PASS": config.PORTAL_DB_PASS,
        "DB_NAME": config.PORTAL_DB_NAME,
}

alarm_db_cfg = {
        "DB_HOST": config.ALARM_DB_HOST,
        "DB_PORT": config.ALARM_DB_PORT,
        "DB_USER": config.ALARM_DB_USER,
        "DB_PASS": config.ALARM_DB_PASS,
        "DB_NAME": config.ALARM_DB_NAME,
}

def connect_db(cfg):
    try:
        conn = MySQLdb.connect(
            host=cfg['DB_HOST'],
            port=cfg['DB_PORT'],
            user=cfg['DB_USER'],
            passwd=cfg['DB_PASS'],
            db=cfg['DB_NAME'],
            use_unicode=True,
            charset="utf8")
        return conn
    except Exception, e:
        logging.getLogger().critical('connect db: %s' % e)
        return None


class DB(object):
    def __init__(self, cfg):
        self.config = cfg
        self.conn = None

    def get_conn(self):
        if self.conn is None:
            self.conn = connect_db(self.config)
        return self.conn

    def execute(self, *a, **kw):
        cursor = kw.pop('cursor', None)
        try:
            cursor = cursor or self.get_conn().cursor()
            cursor.execute(*a, **kw)
        except (AttributeError, MySQLdb.OperationalError):
            self.conn and self.conn.close()
            self.conn = None
            cursor = self.get_conn().cursor()
            cursor.execute(*a, **kw)
        return cursor

    # insert one record in a transaction
    # return last id
    def insert(self, *a, **kw):
        cursor = None
        try:
            cursor = self.execute(*a, **kw)
            row_id = cursor.lastrowid
            self.commit()
            return row_id
        except MySQLdb.IntegrityError:
            self.rollback()
        finally:
            cursor and cursor.close()

    # update in a transaction
    # return affected row count
    def update(self, *a, **kw):
        cursor = None
        try:
            cursor = self.execute(*a, **kw)
            self.commit()
            row_count = cursor.rowcount
            return row_count
        except MySQLdb.IntegrityError:
            self.rollback()
        finally:
            cursor and cursor.close()

    def query_all(self, *a, **kw):
        cursor = None
        try:
            cursor = self.execute(*a, **kw)
            return cursor.fetchall()
        finally:
            cursor and cursor.close()

    def query_one(self, *a, **kw):
        rows = self.query_all(*a, **kw)
        if rows:
            return rows[0]
        else:
            return None

    def query_column(self, *a, **kw):
        rows = self.query_all(*a, **kw)
        if rows:
            return [row[0] for row in rows]
        else:
            return []

    def commit(self):
        if self.conn:
            try:
                self.conn.commit()
            except MySQLdb.OperationalError:
                self.conn = None

    def rollback(self):
        if self.conn:
            try:
                self.conn.rollback()
            except MySQLdb.OperationalError:
                self.conn = None


db = DB(portal_db_cfg)
alarm_db = DB(alarm_db_cfg)
