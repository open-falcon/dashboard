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
