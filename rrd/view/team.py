#-*- coding:utf-8 -*-
import json
from flask import request, g, abort, render_template
from rrd import app
from rrd import config, corelib
from rrd.view.utils import require_login
from rrd.model.team import Team
from rrd.model.user import User

@app.route("/team/<int:team_id>/users", methods=["GET",])
@require_login()
def team_users(team_id):
    if request.method == "GET":
        ret = {"msg":""}

        h = {"Content-type": "application/json"}
        r = corelib.auth_requests(g.user_token, "GET", "%s/team/%s" \
                %(config.API_ADDR, team_id), headers=h)
        if r.status_code != 200:
            ret["msg"] = r.text
            return json.dumps([])
        else:
            j = r.json()
            return json.dumps(j)


@app.route("/team/list", methods=["GET",])
@require_login()
def team_list():
    if request.method == "GET":
        teams = []
        query_term = request.args.get("query", "")
        if query_term:
            d = {
                    "q": query_term,
                    "limit": g.limit or 50,
                    "page": g.page or 1,
            }
        else:
            d = {
                    "q": ".",
                    "limit": g.limit or 50,
                    "page": g.page or 1,
            }

        h = {"Content-type": "application/json"}
        r = corelib.auth_requests(g.user_token, "GET", "%s/team" \
                %(config.API_ADDR,), params=d, headers=h)
        if r.status_code != 200:
            abort(400, "request to api fail: %s" %(r.text,))

        for j in r.json():
            users = [User(x["id"], x["name"], x["cnname"], x["email"], x["phone"], x["im"], x["qq"], x["role"]) for x in j['users']]
            t = Team(j["team"]["id"], j["team"]["name"], j["team"]["resume"], j['creator_name'], users)
            teams.append(t)

        return render_template("team/list.html", **locals())


@app.route("/team/create", methods=["GET", "POST"])
@require_login()
def team_create():
    if request.method == "GET":
        return render_template("team/create.html", **locals())
    
    if request.method == "POST":
        ret = {"msg":""}

        name = request.form.get("name", "")
        resume = request.form.get("resume", "")
        users = request.form.get("users", "")

        user_ids = users and users.split(",") or []
        user_ids = [int(x) for x in user_ids]

        if not name:
            ret["msg"] = "empty name"
            return json.dumps(ret)
        
        h = {"Content-type": "application/json"}
        d = {
                "team_name": name, "resume": resume, "users": user_ids,
        }
        r = corelib.auth_requests(g.user_token ,"POST", "%s/team" %(config.API_ADDR,), \
                data=json.dumps(d), headers=h)
        if r.status_code != 200:
            ret["msg"] = r.text

        return json.dumps(ret)

@app.route("/team/<int:team_id>/edit", methods=["GET", "POST"])
@require_login()
def team_edit(team_id):
    if request.method == "GET":

        h = {"Content-type": "application/json"}
        r = corelib.auth_requests(g.user_token, "GET", "%s/team/%s" \
                %(config.API_ADDR, team_id), headers=h)
        if r.status_code != 200:
            abort(r.status_code, r.text)

        j = r.json()
        team = Team(j['id'], j['name'], j['resume'], j['creator'], [])
        team_user_ids = ",".join([str(x['id']) for x in j['users']])

        return render_template("team/edit.html", **locals())
    
    if request.method == "POST":
        ret = {"msg":""}

        resume = request.form.get("resume", "")
        users = request.form.get("users", "")

        user_ids = users and users.split(",") or []
        user_ids = [int(x) for x in user_ids]

        h = {"Content-type": "application/json"}
        d = {
                "team_id": team_id, "resume": resume, "users": user_ids,
        }
        r = corelib.auth_requests(g.user_token ,"PUT", "%s/team" %(config.API_ADDR,), \
                data=json.dumps(d), headers=h)
        if r.status_code != 200:
            ret["msg"] = r.text

        return json.dumps(ret)

@app.route("/team/<int:team_id>/delete", methods=["POST"])
@require_login(json_msg = "login first")
def team_delete(team_id):
    if request.method == "POST":
        ret = {"msg": ""}
        
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests(g.user_token, "DELETE", "%s/team/%s" \
                %(config.API_ADDR, team_id), headers=h)
        if r.status_code != 200:
            ret['msg'] = "%s:%s" %(r.status_code, r.text)

        return json.dumps(ret)

