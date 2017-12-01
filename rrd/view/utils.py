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
import requests
from flask import g, redirect, session, abort, request

from functools import wraps

from rrd import config 
from rrd import corelib
from rrd.utils import randbytes
from rrd.model.user import User, UserToken

from rrd.utils.logger import logging
log = logging.getLogger(__file__)

def remote_ip():
    if not request.headers.getlist("X-Forward-For"):
        return request.remote_addr
    else:
        return request.headers.getlist("X-Forward-For")[0]

def require_login(redir="/auth/login"):
    def _(f):
        @wraps(f)
        def __(*a, **kw):
            if not g.user:
                return redirect(redir or "/auth/login")
            return f(*a, **kw)
        return __
    return _

def require_login_abort(status_code=403, msg="login first"):
    def _(f):
        @wraps(f)
        def __(*a, **kw):
            if not g.user:
                return abort(status_code, msg)
            return f(*a, **kw)
        return __
    return _

def require_login_json(json_msg={"ok":False, "msg":"login first"}):
    def _(f):
        @wraps(f)
        def __(*a, **kw):
            if not g.user:
                return json.dumps(json_msg)
            return f(*a, **kw)
        return __
    return _

def set_user_cookie(user_token, session_):
    if not user_token:
        return None
    session_[config.SITE_COOKIE] = "%s:%s" % (user_token.name, user_token.sig)

def clear_user_cookie(session_):
    session_[config.SITE_COOKIE] = ""

def get_usertoken_from_session(session_):
    if config.SITE_COOKIE in session_:
        cookies = session_[config.SITE_COOKIE]
        if not cookies:
            return None

        name, sig = cookies.split(":")
        return UserToken(name, sig)

def get_current_user_profile(user_token):
    if not user_token:
        return 

    h = {"Content-type": "application/json"}
    r = corelib.auth_requests("GET", "%s/user/current" %config.API_ADDR, headers=h)
    if r.status_code != 200:
        return

    j = r.json()
    return User(j["id"], j["name"], j["cnname"], j["email"], j["phone"], j["im"], j["qq"], j["role"])

def logout_user(user_token):
    if not user_token:
        return 

    r = corelib.auth_requests("GET", "%s/user/logout" %config.API_ADDR)
    if r.status_code != 200:
        raise Exception("%s:%s" %(r.status_code, r.text))
    clear_user_cookie(session)

def login_user(name, password):
    params = {
        "name": name,
        "password": password,
    }
    r = requests.post("%s/user/login" %config.API_ADDR, data=params)
    if r.status_code != 200:
        raise Exception("%s : %s" %(r.status_code, r.text))

    j = r.json()
    ut = UserToken(j["name"], j["sig"])
    set_user_cookie(ut, session)
    return ut


def ldap_login_user(name, password):
    import ldap
    if not config.LDAP_ENABLED:
        raise Exception("ldap not enabled")

    bind_dn = config.LDAP_BINDDN_FMT
    base_dn = config.LDAP_BASE_DN
    try:
        bind_dn = config.LDAP_BINDDN_FMT %name
    except TypeError: pass

    search_filter = config.LDAP_SEARCH_FMT
    try:
        search_filter = config.LDAP_SEARCH_FMT %name
    except TypeError: pass

    cli = None
    try:
        ldap_server = config.LDAP_SERVER if (config.LDAP_SERVER.startswith("ldap://") or config.LDAP_SERVER.startswith("ldaps://")) else "ldaps://%s" % config.LDAP_SERVER if config.LDAP_TLS_START_TLS else "ldap://%s" % config.LDAP_SERVER
        log.debug("ldap_server:%s bind_dn:%s base_dn:%s filter:%s attrs:%s" %(ldap_server, bind_dn, config.LDAP_BASE_DN, search_filter, config.LDAP_ATTRS))
        cli = ldap.initialize(ldap_server)
        cli.protocol_version = ldap.VERSION3
        if config.LDAP_TLS_START_TLS or ldap_server.startswith('ldaps://'):
            if config.LDAP_TLS_CACERTFILE:
                cli.set_option(ldap.OPT_X_TLS_CACERTFILE, config.LDAP_TLS_CACERTFILE)
            if config.LDAP_TLS_CERTFILE:
                cli.set_option(ldap.OPT_X_TLS_CERTFILE, config.LDAP_TLS_CERTFILE)
            if config.LDAP_TLS_KEYFILE:
                cli.set_option(ldap.OPT_X_TLS_KEYFILE, config.LDAP_TLS_KEYFILE)
            if config.LDAP_TLS_REQUIRE_CERT:
                cli.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, config.LDAP_TLS_REQUIRE_CERT)
            if config.LDAP_TLS_CIPHER_SUITE:
                cli.set_option(ldap.OPT_X_TLS_CIPHER_SUITE, config.LDAP_TLS_CIPHER_SUITE)
        cli.simple_bind_s(bind_dn, password)
        result = cli.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter, config.LDAP_ATTRS)
        log.debug("ldap result: %s" % result)
        d = result[0][1]
        email = d['mail'][0]
        cnname = d['cn'][0]
        if 'sn' in d and 'givenName' in d:
            cnname = d['givenName'][0] + ' ' + d['sn'][0]
        if 'displayName' in d:
            cnname = d['displayName'][0]
        if 'telephoneNumber' in d:
            phone = d['telephoneNumber'] and d['telephoneNumber'][0] or ""
        else:
            phone = ""
    
        return {
                "name": name,
                "password": password,
                "cnname": cnname,
                "email": email,
                "phone": phone,
        }
    except ldap.LDAPError as e:
        cli and cli.unbind_s()
        raise e
    except (IndexError, KeyError) as e:
        raise e
    finally:
        cli and cli.unbind_s()
