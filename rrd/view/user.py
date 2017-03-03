#-*- coding:utf-8 -*-
import json
from flask import request, g, abort, render_template
from rrd import app
from rrd import corelib
from rrd import config
from rrd.view.utils import require_login
from rrd.model.user import User

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
@require_login(json_msg = "please login first")
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
@require_login(json_msg = "please login first")
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
@require_login()
def user_list():
    if request.method == "GET":
        query_term = request.args.get("query", "")
        users = []
        if query_term:
            d = {
                    "q": query_term,
                    "limit": g.limit or 50,
                    "page": g.page or 1,
            }
            h = {"Content-type":"application/json"}
            r = corelib.auth_requests(g.user_token, "GET", "%s/user/users" \
                    %(config.API_ADDR,), params=d, headers=h)
            if r.status_code != 200:
                abort(400, "request to api fail: %s" %(r.text,))
            j = r.json() or []
            for x in j:
                u = User(x["id"], x["name"], x["cnname"], x["email"], x["phone"], x["im"], x["qq"], x["role"])
                users.append(u)

        return render_template("user/list.html", **locals())

@app.route("/user/query", methods=["GET",])
@require_login(json_msg="login first")
def user_query():
    if request.method == "GET":
        query_term = request.args.get("query", "")
        if query_term:
            d = {
                    "q": query_term,
                    "limit": g.limit or 50,
                    "page": g.page or 1,
            }
            h = {"Content-type":"application/json"}
            r = corelib.auth_requests(g.user_token, "GET", "%s/user/users" \
                    %(config.API_ADDR,), params=d, headers=h)
            if r.status_code != 200:
                ret['msg'] = t.text
                return json.dumps(ret)

            j = r.json() or []
            return json.dumps({"users": j})

@app.route("/user/create", methods=["GET", "POST"])
@require_login()
def user_create():
    if request.method == "GET":
        return render_template("user/create.html", **locals())
    
    if request.method == "POST":
        ret = {"msg":""}

        name = request.form.get("name", "")
        cnname = request.form.get("cnname", "")
        password = request.form.get("password", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        im = request.form.get("im", "")
        qq = request.form.get("qq", "")

        if not name or not cnname or not password or not email:
            ret["msg"] = "not all form item entered"
            return json.dumps(ret)
        
        h = {"Content-type": "application/json"}
        d = {
                "name": name, "cnname": cnname, "password": password, "email": email, "phone": phone, "im": im, "qq": qq,
        }
        r = corelib.auth_requests(g.user_token ,"POST", "%s/user/create" %(config.API_ADDR,), \
                data=json.dumps(d), headers=h)
        if r.status_code != 200:
            ret["msg"] = r.text

        return json.dumps(ret)

##admin
@app.route("/admin/user/<int:user_id>/edit", methods=["GET", "POST"])
@require_login()
def admin_user_edit(user_id):
    if request.method == "GET":
        if not (g.user.is_admin() or g.user.is_root()):
            abort(403, "no such privilege")

        h = {"Content-type":"application/json"}
        r = corelib.auth_requests(g.user_token ,"GET", "%s/user/u/%s" %(config.API_ADDR, user_id), headers=h)
        if r.status_code != 200:
            abort(r.status_code, r.text)
        j = r.json()
        user = j and User(j["id"], j["name"], j["cnname"], j["email"], j["phone"], j["im"], j["qq"], j["role"])

        if not user:
            abort(404, "no such user where id=%s" % user_id)

        return render_template("user/edit.html", **locals())
    
    if request.method == "POST":
        ret = {"msg":""}

        if not (g.user.is_admin() or g.user.is_root()):
            ret["msg"] = "no such privilege"
            return json.dumps(ret)

        user_id = request.form.get("id", "")
        cnname = request.form.get("cnname", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        im = request.form.get("im", "")
        qq = request.form.get("qq", "")

        h = {"Content-type": "application/json"}
        d = {
                "user_id": user_id, "cnname": cnname, "email": email, "phone": phone, "im": im, "qq": qq,
        }
        r = corelib.auth_requests(g.user_token ,"PUT", "%s/admin/change_user_profile" %(config.API_ADDR,), \
                data=json.dumps(d), headers=h)
        if r.status_code != 200:
            ret["msg"] = r.text

        return json.dumps(ret)

@app.route("/admin/user/<int:user_id>/chpwd", methods=["POST", ])
@require_login(json_msg="login first")
def admin_user_change_password(user_id):
    if request.method == "POST":
        ret = {"msg": ""}

        if not (g.user.is_admin or g.user.is_root()):
            ret["msg"] = "you do not have permissions"
            return json.dumps(ret)

        password = request.form.get("password")
        if not password:
            ret["msg"] = "no password entered"
            return json.dumps(ret)

        h = {"Content-type": "application/json"}
        d = {
                "user_id": user_id, "password": password,
        }
        r = corelib.auth_requests(g.user_token ,"PUT", "%s/admin/change_user_passwd" %(config.API_ADDR,), \
                data=json.dumps(d), headers=h)
        if r.status_code != 200:
            ret["msg"] = r.text

        return json.dumps(ret)

@app.route("/admin/user/<int:user_id>/role", methods=["POST", ])
@require_login(json_msg="login first")
def admin_user_change_role(user_id):
    if request.method == "POST":
        ret = {"msg": ""}

        if not (g.user.is_admin or g.user.is_root()):
            ret["msg"] = "you do not have permissions"
            return json.dumps(ret)

        role = str(request.form.get("role", ""))
        if not role or role not in ['1', '0']:
            ret["msg"] = "invalid role"
            return json.dumps(ret)

        admin = "yes" if role == '1' else "no"

        h = {"Content-type":"application/json"}
        d = {"admin": admin, "user_id": int(user_id)}

        r = corelib.auth_requests(g.user_token, "PUT", "%s/admin/change_user_role" \
                %(config.API_ADDR,), data=json.dumps(d), headers=h)
        if r.status_code != 200:
            ret["msg"] = r.text

        return json.dumps(ret)

@app.route("/admin/user/<int:user_id>/delete", methods=["POST", ])
@require_login(json_msg="login first")
def admin_user_delete(user_id):
    if request.method == "POST":
        ret = {"msg": ""}

        if not (g.user.is_admin or g.user.is_root()):
            ret["msg"] = "you do not have permissions"
            return json.dumps(ret)

        h = {"Content-type":"application/json"}
        d = {"user_id": int(user_id)}

        r = corelib.auth_requests(g.user_token, "DELETE", "%s/admin/delete_user" \
                %(config.API_ADDR,), data=json.dumps(d), headers=h)
        if r.status_code != 200:
            ret["msg"] = r.text

        return json.dumps(ret)
