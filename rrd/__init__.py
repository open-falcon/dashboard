#-*- coding:utf-8 -*-
import os
import traceback
from flask import Flask

#-- create app --
app = Flask(__name__)
app.config.from_object("rrd.config")

from rrd.utils.logger import logging
log = logging.getLogger(__file__)

@app.errorhandler(Exception)
def all_exception_handler(error):
    tb = traceback.format_exc()
    err_msg = '<pre>dashboard 暂时无法访问,请联系管理员.\n\nerror: %s\n\ntraceback日志如下:\n%s</pre>' %(error, tb)
    return err_msg, 500

from view import index
from view import auth
from view import user, team
from view import api
from view import chart, screen
