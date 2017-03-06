#-*- coding:utf-8 -*-
import os
import traceback
from flask import Flask

#-- create app --
app = Flask(__name__)
app.config.from_object("rrd.config")

@app.errorhandler(Exception)
def all_exception_handler(error):
    print traceback.format_exc()
    return u'dashboard 暂时无法访问，请联系管理员', 500

from view import index
from view import api
from view import chart, screen
from view import auth, user, team
