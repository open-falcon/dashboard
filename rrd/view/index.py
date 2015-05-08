#-*- coding:utf-8 -*-
from flask import render_template
from rrd import app

@app.route("/")
def index():
    return render_template("index.html", **locals())
