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
from rrd import config
from flask import render_template, request, g
from rrd.model.portal.host_group import HostGroup

from rrd.utils.logger import logging
log = logging.getLogger(__file__)

@app.route('/portal/hostgroup', methods=["GET",])
def home_get():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 10))
    query = request.args.get('q', '').strip()
    mine = request.args.get('mine', '1')
    me = g.user.name if mine == '1' else None
    vs, total = HostGroup.query(page, limit, query, me)
    log.debug(vs)
    return render_template(
        'portal/group/index.html',
        data={
            'vs': vs,
            'total': total,
            'query': query,
            'limit': limit,
            'page': page,
            'mine': mine,
            'is_root': g.user.name in config.MAINTAINERS,
        }
    )

