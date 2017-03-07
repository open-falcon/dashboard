#-*- coding:utf-8 -*-
from flask import request, g, abort, render_template, redirect
import requests
import json
from rrd import app
from rrd import config
from rrd.view import utils as view_utils
from rrd.view.utils import require_login

from rrd.utils.logger import logging
log = logging.getLogger(__file__)

@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        if g.user:
            return redirect("/")

        return render_template("auth/login.html", **locals())

    if request.method == "POST":
        ret = { "msg": "", }

        name = request.form.get("name")
        password = request.form.get("password")
        if not name or not password:
            ret["msg"] = "no name or password"
            return json.dumps(ret)

        try:
            ut = view_utils.login_user(name, password)
            if not ut:
                ret["msg"] = "no such user"
                return json.dumps(ret)

            ret["data"] = {
                    "name": ut.name,
                    "sig": ut.sig,
            }
            return json.dumps(ret)
        except Exception as e:
            ret["msg"] = str(e)
            return json.dumps(ret)

@app.route("/auth/logout", methods=["GET",])
@require_login()
def auth_logout():
    if request.method == "GET":
        view_utils.logout_user(g.user_token)
        return redirect("/auth/login")

@app.route("/auth/register", methods=["GET", "POST"])
def auth_register():
    if request.method == "GET":
        if g.user:
            return redirect("/auth/login")
        return render_template("auth/register.html", **locals())

    if request.method == "POST":
        ret = {"msg":""}

        name = request.form.get("name", "")
        cnname = request.form.get("cnname", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        repeat_password = request.form.get("repeat_password", "")

        if not name or not password or not email or not cnname:
            ret["msg"] = "not all form item entered"
            return json.dumps(ret)

        if password != repeat_password:
            ret["msg"] = "repeat password not equal"
            return json.dumps(ret)

        h = {"Content-type":"application/json"}
        d = {
            "name": name,
            "cnname": cnname,
            "email": email,
            "password": password,
        }

        r = requests.post("%s/user/create" %(config.API_ADDR,), \
                data=json.dumps(d), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            ret['msg'] = r.text

        return json.dumps(ret)
