# -*- coding:utf-8 -*-
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


__author__ = 'Ulric Qin'
from rrd import app
from flask import render_template, request
from rrd.utils import random_string
from rrd.model.portal.alert_link import AlertLink

@app.route('/portal/links/<path>', methods=["GET",])
def portal_links(path):
    vs = AlertLink.select_vs(where='path=%s', params=[path])
    sms_strings = []
    if vs:
        sms_strings = vs[0].content.split(',,')
    return render_template('portal/alert_link/index.html', **locals())


@app.route('/portal/links/store', methods=['POST'])
def portal_links_store():
    sms_strings = request.get_data()
    path = random_string(8)
    ids = AlertLink.column('id', where='path=%s', params=[path])
    if ids:
        AlertLink.update_dict({'content': sms_strings}, where='id=%s', params=[ids[0]])
    else:
        AlertLink.insert({'path': path, 'content': sms_strings})

    return path
