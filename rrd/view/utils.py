#-*- coding:utf-8 -*-
import json
import requests
from flask import g, redirect, session

from functools import wraps

from rrd import config 
from rrd import corelib
from rrd.utils import randbytes
from rrd.model.user import User, UserToken

def require_login(redir="/auth/login", json_msg="", html_msg=""):
    def _(f):
        @wraps(f)
        def __(*a, **kw):
            if not g.user:
                if redir:
                    return redirect(redir)
                elif json_msg:
                    return json.dumps({"msg": json_msg})
                elif html_msg:
                    return abort(403, html_msg)
                else:
                    return abort(403, "please login first")
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
    r = corelib.auth_requests(user_token, "GET", "%s/user/current" %config.API_ADDR, headers=h)
    if r.status_code != 200:
        return

    j = r.json()
    return User(j["id"], j["name"], j["cnname"], j["email"], j["phone"], j["im"], j["qq"], j["role"])

def logout_user(user_token):
    if not user_token:
        return 

    r = corelib.auth_requests(user_token, "GET", "%s/user/logout" %config.API_ADDR)
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

