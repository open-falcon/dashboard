#-*- coding:utf-8 -*-
import json
import requests
from flask import g, redirect, session, abort, request

from functools import wraps

from rrd import config 
from rrd import corelib
from rrd.utils import randbytes
from rrd.model.user import User, UserToken

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
        raise Exception("{} : {}".format(r.status_code, r.text))

    j = r.json()
    ut = UserToken(j["name"], j["sig"])
    set_user_cookie(ut, session)
    return ut

