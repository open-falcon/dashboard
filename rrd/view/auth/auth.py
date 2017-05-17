#-*- coding:utf-8 -*-
from flask import request, g, abort, render_template, redirect
import requests
import json
from rrd import app
from rrd import config
from rrd.view import utils as view_utils

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
        ldap = request.form.get("ldap") or "0"

        if not name or not password:
            ret["msg"] = "no name or password"
            return json.dumps(ret)

        if ldap == "1":
            try:
                ldap_info = view_utils.ldap_login_user(name, password)

                #query user by name
                server_side_header = {"Content-type":"application/json",
                                 "apiToken": "{\"name\":\"root\",\"sig\":\"%s\"}" % config.PLUS_API_TOKEN
                                 }
                r = requests.get("%s/user/name/%s" %(config.API_ADDR, name), headers=server_side_header)
                log.debug("%s:%s" %(r.status_code, r.text))

                #record not found
                if r.status_code < 400:
                    user = json.loads(r.text)

                else:
                    user = None
                    h = {"Content-type": "application/json"}
                    d = {
                        "name": name,
                        "password": password,
                        "cnname": ldap_info['cnname'],
                        "email": ldap_info['email'],
                        "phone": ldap_info['phone'],
                    }

                    r = requests.post("%s/user/create" % (config.API_ADDR,), \
                                      data=json.dumps(d), headers=h)
                    log.debug("%s:%s" % (r.status_code, r.text))


                #update user info from ldap
                #log.debug(ldap_info)
                if ldap_info["phone"] != user["phone"] or user["cnname"] == "" or user["email"] != ldap_info["email"]:
                    new_user = {
                        "name": name,
                        "cnname": ldap_info['cnname'],
                        "email": ldap_info['email'],
                        "im": user["im"],
                        "phone": ldap_info['phone'],
                        "qq": user["qq"]
                    }
                    current_user_header = {"Content-type": "application/json",
                                     "apiToken": "{\"name\":\"%s\",\"sig\":\"%s\"}" % (name, config.PLUS_API_TOKEN)
                                           }
                    r = requests.put("%s/user/update" % (config.API_ADDR),
                                     data=json.dumps(new_user), headers=current_user_header)
                    log.debug("%s:%s" % (r.status_code, r.text))

                ut = None
                try:
                    #login with name/password
                    #if invalid password, exception is raised
                    ut = view_utils.login_user(name, password)
                    # update password in db if ldap password changed
                except Exception as e:
                    log.debug(e)

                #update password of falcon user with ldap password if login failed for the first time
                if not ut and user:
                    change_user_passwd_data = {
                        "user_id": user["id"],
                        "password": password
                    }

                    r = requests.put("%s/admin/change_user_passwd" % (config.API_ADDR),
                                     data=json.dumps(change_user_passwd_data), headers=server_side_header)
                    log.debug("%s:%s" % (r.status_code, r.text))
                else:
                    ret["data"] = {
                        "name": ut.name,
                        "sig": ut.sig,
                    }
                    return json.dumps(ret)

            except Exception as e:
                ret["msg"] = str(e)
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
