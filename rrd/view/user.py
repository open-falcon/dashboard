#-*- coding:utf-8 -*-
import json
from flask import request, g, abort, render_template
from rrd import app
from rrd import corelib
from rrd import config
from rrd.view.utils import require_login

@app.route("/user/about/<username>", methods=["GET",])
@require_login()
def user_info(username):
    if request.method == "GET":
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests(g.user_token, "GET", "%s/user/u/%s" %(config.API_ADDR, username), headers=h)
        if r.status_code != 200:
            abort(400, "%s:%s" %(r.status_code, r.text))
        user_info = r.json()
        return render_template("user/about.html", **locals())

@app.route("/user/profile", methods=["GET", "POST"])
@require_login()
def user_profile():
    if request.method == "GET":
        current_user = g.user
        return render_template("user/profile.html", **locals())

    if request.method == "POST":
        ret = {"msg":""}

        name = g.user.name
        cnname = request.form.get("cnname", "")
        email = request.form.get("email", "")
        im = request.form.get("im", "")
        phone = request.form.get("phone", "")
        qq = request.form.get("qq", "")

        h = {"Content-type": "application/json"}
        d = {
                "name": name,
                "cnname": cnname,
                "email": email,
                "im": im,
                "phone": phone,
                "qq": qq,
        }

        r = corelib.auth_requests(g.user_token, "PUT", "%s/user/update" %(config.API_ADDR,), \
                data=json.dumps(d), headers=h)
        if r.status_code != 200:
            ret["msg"] = r.text

        return json.dumps(ret)

@app.route("/user/chpwd", methods=["POST", ])
@require_login()
def user_change_passwd():
    if request.method == "POST":
        ret = {"msg": ""}

        old_password = request.form.get("old_password", "")
        new_password = request.form.get("new_password", "")
        repeat_password = request.form.get("repeat_password", "")
        if not (old_password and new_password and repeat_password):
            ret["msg"] = "some form item missing"
            return json.dumps(ret)

        if new_password != repeat_password:
            ret["msg"] = "repeat and new password not equal"
            return json.dumps(ret)

        h = {"Content-type":"application/json"}
        d = {
            "old_password": old_password,
            "new_password": new_password,
        }

        r = corelib.auth_requests(g.user_token, "PUT", "%s/user/cgpasswd" %(config.API_ADDR,), \
                data=json.dumps(d), headers=h)
        if r.status_code != 200:
            ret['msg'] = r.text

        return json.dumps(ret)
        

@app.route("/user/list", methods=["GET",])
def user_list():
    if request.method == "GET":
        return render_template("user/list.html", **locals())

@app.route("/user/create", methods=["GET", "POST"])
def user_create():
    if request.method == "GET":
        return render_template("user/create.html", **locals())
    
    if request.method == "POST":
        pass
