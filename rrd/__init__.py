#-*- coding:utf-8 -*-
import os
import traceback
from flask import Flask

#-- create app --
app = Flask(__name__)
app.config.from_object("rrd.config")

@app.errorhandler(Exception)
def all_exception_handler(error):
    tb = traceback.format_exc()
    err_msg = '<pre>暂时无法访问,请联系管理员.\n\nerror: %s\n\ntraceback日志如下:\n%s</pre>' %(error, tb)
    return err_msg, 500

from view import index
from view.auth import auth
from view.user import user
from view.team import team
from view.dashboard import chart, screen
from view.portal import *
