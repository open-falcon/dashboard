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


import json
from rrd import corelib
from rrd import config

from rrd.utils.logger import logging
log = logging.getLogger(__file__)

class UserToken(object):
    def __init__(self, name, sig):
        self.name = name
        self.sig = sig
    
    def __repr__(self):
        return "<UserToken name=%s, sig=%s>"  % (self.name, self.sig)
    __str__ = __repr__

class User(object):
    def __init__(self, id, name, cnname, email, phone, im, qq, role):
        self.id = id
        self.name = name
        self.cnname = cnname
        self.email = email
        self.phone = phone
        self.im = im
        self.qq = qq
        self.role = role

    def __repr__(self):
        return "<User id=%s, name=%s, cnname=%s>" \
                % (self.id, self.name, self.cnname)
    __str__ = __repr__

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cnname': self.cnname,
            'email': self.email,
            'phone': self.phone,
            'im': self.im,
            'qq': self.qq,
            'role': self.role,
        }

    def is_root(self):
        return str(self.role) == "2"

    def is_admin(self):
        return str(self.role) == "1"

    def in_teams(self, groups=[]):
        if not groups:
            return False

        r = corelib.auth_requests("GET", '%s/user/u/%s/in_teams?team_names=%s' \
                % (config.API_ADDR, self.id, ','.join(groups))) 
        log.debug("%s:%s" %(r.status_code, r.text))
        if r.status_code != 200:
            return False
        j = r.json()
        return j["message"] == "true"

    @classmethod
    def get_by_id(cls, user_id):
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("GET", "%s/user/u/%s" %(config.API_ADDR, user_id), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))
        j = r.json()
        return j and cls(j['id'], j['name'], j['cnname'], j['email'], j['phone'], j['im'], j['qq'], j['role'])

    @classmethod
    def get_by_name(cls, name):
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("GET", "%s/user/name/%s" %(config.API_ADDR, name), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))
        j = r.json()
        return j and cls(j['id'], j['name'], j['cnname'], j['email'], j['phone'], j['im'], j['qq'], j['role'])

    @classmethod
    def update_user_profile(cls, data={}):
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("PUT", "%s/user/update" %(config.API_ADDR,), \
                data=json.dumps(data), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))
        return r.text
            
    @classmethod
    def change_user_passwd(cls, old_password, new_password):
        h = {"Content-type":"application/json"}
        d = {
            "old_password": old_password,
            "new_password": new_password,
        }

        r = corelib.auth_requests("PUT", "%s/user/cgpasswd" %(config.API_ADDR,), \
                data=json.dumps(d), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))
        return r.text

    @classmethod
    def get_users(cls, query_term, limit=20, page=1):
        users = []

        if not query_term:
            query_term = '.'

        d = {
            "q": query_term,
            "limit": limit,
            "page": page,
        }
        h = {"Content-type":"application/json"}
        r = corelib.auth_requests("GET", "%s/user/users" \
                %(config.API_ADDR,), params=d, headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))

        j = r.json() or []
        for x in j:
            u = cls(x["id"], x["name"], x["cnname"], x["email"], x["phone"], x["im"], x["qq"], x["role"])
            users.append(u)

        return users

    #anyone can create user
    @classmethod
    def create_user(cls, name, cnname, password, email, phone="", im="", qq=""):
        h = {"Content-type": "application/json"}
        d = {
            "name": name, "cnname": cnname, "password": password, "email": email, "phone": phone, "im": im, "qq": qq,
        }
        r = corelib.auth_requests("POST", "%s/user/create" %(config.API_ADDR,), \
                data=json.dumps(d), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))
        return r.json()

    @classmethod
    def admin_update_user_profile(cls, data={}):
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("PUT", "%s/admin/change_user_profile" %(config.API_ADDR,), \
                data=json.dumps(data), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))
        return r.text

    @classmethod
    def admin_change_user_passwd(cls, user_id, password):
        h = {"Content-type": "application/json"}
        d = {
            "user_id": user_id, "password": password,
        }
        r = corelib.auth_requests("PUT", "%s/admin/change_user_passwd" %(config.API_ADDR,), \
                data=json.dumps(d), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))
        return r.text

    @classmethod
    def admin_change_user_role(cls, user_id, admin):
        h = {"Content-type":"application/json"}
        d = {"admin": admin, "user_id": user_id}

        r = corelib.auth_requests("PUT", "%s/admin/change_user_role" \
                %(config.API_ADDR,), data=json.dumps(d), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))
        return r.text
    
    @classmethod
    def admin_delete_user(cls, user_id):
        h = {"Content-type":"application/json"}
        d = {"user_id": int(user_id)}
        r = corelib.auth_requests("DELETE", "%s/admin/delete_user" \
                %(config.API_ADDR,), data=json.dumps(d), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))
        return r.text
