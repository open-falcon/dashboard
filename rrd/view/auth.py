#-*- coding:utf-8 -*-
from flask import request, g, abort, render_template
from rrd import app
from rrd.view import utils as view_utils

import requests
import json

@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
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

@app.route("/auth/logout", methods=["POST",])
def auth_logout():
    if request.method == "POST":
        pass

@app.route("/auth/register", methods=["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/register.html", **locals())

    if request.method == "POST":
        pass
