#-*- coding:utf-8 -*-
from flask import jsonify, render_template, request, g
from rrd import app

@app.route("/portal/alarm-dash")
def alarm_dash_get():
    return render_template("portal/alarm/index.html", **locals())
