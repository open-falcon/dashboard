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
from flask import request, g, abort, render_template
from rrd import app
from rrd.model.team import Team

@app.route("/team/<int:team_id>/users", methods=["GET",])
def team_users(team_id):
    if request.method == "GET":
        try:
            ret = Team.get_team_users(team_id)
        except Exception as e:
            ret = {"msg":str(e)}
        return json.dumps(ret)

@app.route("/team/<team_name>/users", methods=["GET",])
def team_users_by_name(team_name):
    if request.method == "GET":
        try:
            ret = Team.get_team_users_by_name(team_name)
        except Exception as e:
            ret = {"msg":str(e)}
        return json.dumps(ret)

@app.route("/team/list", methods=["GET",])
def team_list():
    if request.method == "GET":
        query_term = request.args.get("query", "")
        teams = Team.get_teams(query_term, g.limit or 20, g.page or 1)
        return render_template("team/list.html", **locals())


@app.route("/team/create", methods=["GET", "POST"])
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
        
        try:
            Team.create_team(name, resume, user_ids)
        except Exception as e:
            ret['msg'] = str(e)
        return json.dumps(ret)

@app.route("/team/<int:team_id>/edit", methods=["GET", "POST"])
def team_edit(team_id):
    if request.method == "GET":
        j = Team.get_team_users(team_id)
        team = Team(j['id'], j['name'], j['resume'], j['creator'], j['creator_name'], [])
        team_user_ids = ",".join([str(x['id']) for x in j['users']])

        return render_template("team/edit.html", **locals())
    
    if request.method == "POST":
        ret = {"msg":""}

        resume = request.form.get("resume", "")
        users = request.form.get("users", "")

        user_ids = users and users.split(",") or []
        user_ids = [int(x) for x in user_ids]

        try:
            Team.update_team(team_id, resume, user_ids)
        except Exception as e:
            ret['msg'] = str(e)
        return json.dumps(ret)

@app.route("/team/<int:team_id>/delete", methods=["POST"])
def team_delete(team_id):
    if request.method == "POST":
        ret = {"msg": ""}
        try:
            Team.delete_team(team_id)
        except Exception as e:
            ret['msg'] = str(e)
        return json.dumps(ret)

