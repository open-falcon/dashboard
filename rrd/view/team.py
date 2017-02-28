#-*- coding:utf-8 -*-
from flask import request, g, abort, render_template
from rrd import app

@app.route("/team", methods=["GET", "POST"])
def account_team():
    if request.method == "GET":
        return render_template("team/list.html", **locals())

    if request.method == "POST":
        pass

