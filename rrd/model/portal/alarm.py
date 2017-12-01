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


from .bean import Bean
from rrd.store import alarm_db

class Event(Bean):
    _db = alarm_db
    _tbl = 'events'
    _cols = 'id, event_caseId, step, cond, status, timestamp'

    def __init__(self, id, event_caseId, step, cond, status, timestamp):
        self.id = id
        self.event_caseId = event_caseId
        self.step = step
        self.cond = cond
        self.status = status
        self.timestamp = timestamp
    
    @classmethod
    def query(cls, page, limit, event_caseId):
        where = 'event_caseId = %s'
        params = [event_caseId]
        
        vs = cls.select_vs(where=where, params=params, page=page, limit=limit, order='timestamp desc')
        total = cls.total(where, params)

        return vs, total


class EventCase(Bean):
    _db = alarm_db
    _tbl = 'event_cases'
    _cols = 'id, endpoint, metric, func, cond, note, max_step, current_step, priority, status, timestamp, update_at, closed_at, closed_note, user_modified, tpl_creator, expression_id, strategy_id, template_id, process_note, process_status'

    def __init__(self, id, endpoint, metric, func, cond, note, max_step, current_step, priority,\
            status, timestamp, update_at, closed_at, closed_note, user_modified, tpl_creator, \
            expression_id, strategy_id, template_id, process_note, process_status):
        self.id = id
        self.endpoint = endpoint
        self.metric = metric
        self.func = func
        self.cond = cond
        self.note = note
        self.max_step = max_step
        self.current_step = current_step
        self.priority = priority
        self.status = status
        self.timestamp = timestamp
        self.update_at = update_at
        self.closed_at = closed_at
        self.closed_note = closed_note
        self.user_modified = user_modified
        self.tpl_creator = tpl_creator
        self.expression_id = expression_id
        self.strategy_id = strategy_id
        self.template_id = template_id
        self.process_note = process_note
        self.process_status = process_status

    @classmethod
    def query(cls, page, limit, endpoint_query, metric_query, status):
        where = '1=1'
        params = []
        if status == "PROBLEM" or status == "OK":
            where = 'status = %s'
            params = [status]

        if endpoint_query != "":
            where += ' and endpoint like %s'
            params.append('%' + endpoint_query + '%')

        if metric_query != "":
            where += ' and metric like %s'
            params.append('%' + metric_query + '%')

        vs = cls.select_vs(where=where, params=params, page=page, limit=limit, order='update_at desc')
        total = cls.total(where, params)

        return vs, total

class EventNote(Bean):
    _db = alarm_db
    _tbl = 'event_note'
    _cols = 'id, event_caseId, note, case_id, status, timestamp, user_id'

    def __init__(self, id, event_caseId, note, case_id, status, timestamp, user_id):
        self.id = id
        self.event_caseId = event_caseId
        self.note = note
        self.case_id = case_id
        self.status = status
        self.timestamp = timestamp
        self.user_id = user_id

#desc events;
#+--------------+------------------+------+-----+-------------------+-----------------------------+
#| Field        | Type             | Null | Key | Default           | Extra                       |
#+--------------+------------------+------+-----+-------------------+-----------------------------+
#| id           | mediumint(9)     | NO   | PRI | NULL              | auto_increment              |
#| event_caseId | varchar(50)      | YES  | MUL | NULL              |                             |
#| step         | int(10) unsigned | YES  |     | NULL              |                             |
#| cond         | varchar(200)     | NO   |     | NULL              |                             |
#| status       | int(3) unsigned  | YES  |     | 0                 |                             |
#| timestamp    | timestamp        | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
#+--------------+------------------+------+-----+-------------------+-----------------------------+
#
#desc event_note;
#+--------------+------------------+------+-----+-------------------+-----------------------------+
#| Field        | Type             | Null | Key | Default           | Extra                       |
#+--------------+------------------+------+-----+-------------------+-----------------------------+
#| id           | mediumint(9)     | NO   | PRI | NULL              | auto_increment              |
#| event_caseId | varchar(50)      | YES  | MUL | NULL              |                             |
#| note         | varchar(300)     | YES  |     | NULL              |                             |
#| case_id      | varchar(20)      | YES  |     | NULL              |                             |
#| status       | varchar(15)      | YES  |     | NULL              |                             |
#| timestamp    | timestamp        | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
#| user_id      | int(10) unsigned | YES  | MUL | NULL              |                             |
#+--------------+------------------+------+-----+-------------------+-----------------------------+
#
#desc event_cases;
#+----------------+------------------+------+-----+-------------------+-----------------------------+
#| Field          | Type             | Null | Key | Default           | Extra                       |
#+----------------+------------------+------+-----+-------------------+-----------------------------+
#| id             | varchar(50)      | NO   | PRI | NULL              |                             |
#| endpoint       | varchar(100)     | NO   | MUL | NULL              |                             |
#| metric         | varchar(200)     | NO   |     | NULL              |                             |
#| func           | varchar(50)      | YES  |     | NULL              |                             |
#| cond           | varchar(200)     | NO   |     | NULL              |                             |
#| note           | varchar(500)     | YES  |     | NULL              |                             |
#| max_step       | int(10) unsigned | YES  |     | NULL              |                             |
#| current_step   | int(10) unsigned | YES  |     | NULL              |                             |
#| priority       | int(6)           | NO   |     | NULL              |                             |
#| status         | varchar(20)      | NO   |     | NULL              |                             |
#| timestamp      | timestamp        | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
#| update_at      | timestamp        | YES  |     | NULL              |                             |
#| closed_at      | timestamp        | YES  |     | NULL              |                             |
#| closed_note    | varchar(250)     | YES  |     | NULL              |                             |
#| user_modified  | int(10) unsigned | YES  |     | NULL              |                             |
#| tpl_creator    | varchar(64)      | YES  |     | NULL              |                             |
#| expression_id  | int(10) unsigned | YES  |     | NULL              |                             |
#| strategy_id    | int(10) unsigned | YES  |     | NULL              |                             |
#| template_id    | int(10) unsigned | YES  |     | NULL              |                             |
#| process_note   | mediumint(9)     | YES  |     | NULL              |                             |
#| process_status | varchar(20)      | YES  |     | unresolved        |                             |
#+----------------+------------------+------+-----+-------------------+-----------------------------+
