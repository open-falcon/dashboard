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
from flask import request, g, jsonify, render_template
from rrd.model.portal.host_group import HostGroup
from rrd.model.portal.grp_tpl import GrpTpl
from rrd.service import group_service


@app.route('/portal/group/create', methods=['POST'])
def group_create_post():
    grp_name = request.form['grp_name'].strip()
    if not grp_name:
        return jsonify(msg="group name is blank")

    grp_id = HostGroup.create(grp_name, g.user.name, 1)
    if grp_id > 0:
        return jsonify(msg='')
    else:
        return jsonify(msg='grp_name has already existent')


@app.route('/portal/group/delete/<group_id>')
def group_delete_get(group_id):
    group_id = int(group_id)
    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group')

    if not group.writable(g.user):
        return jsonify(msg='no permission')

    return jsonify(msg=group_service.delete_group(group_id))


@app.route('/portal/group/update/<group_id>', methods=['POST'])
def group_update_post(group_id):
    group_id = int(group_id)
    new_name = request.form['new_name'].strip()
    if not new_name:
        return jsonify(msg='new name is blank')

    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group')

    if not group.writable(g.user):
        return jsonify(msg='no permission')

    HostGroup.update_dict({'grp_name': new_name}, 'id=%s', [group_id])
    return jsonify(msg='')


@app.route('/portal/group/advanced')
def group_advanced_get():
    return render_template('portal/group/advanced.html')


@app.route('/portal/group/rename', methods=['POST'])
def group_rename_post():
    old_str = request.form['old_str'].strip()
    new_str = request.form['new_str'].strip()
    if not old_str:
        return jsonify(msg='old is blank')

    return jsonify(msg=group_service.rename(old_str, new_str, g.user.name))


@app.route('/portal/group/templates/<grp_id>')
def group_templates_get(grp_id):
    grp_id = int(grp_id)
    grp = HostGroup.read(where='id = %s', params=[grp_id])
    if not grp:
        return jsonify(msg='no such group')

    ts = GrpTpl.tpl_list(grp_id)

    return render_template('portal/group/templates.html', group=grp, ts=ts)


@app.route('/portal/group/bind/template')
def group_bind_template_get():
    tpl_id = request.args.get('tpl_id', '').strip()
    grp_id = request.args.get('grp_id', '').strip()
    if not tpl_id:
        return jsonify(msg="tpl id is blank")

    if not grp_id:
        return jsonify(msg="grp id is blank")

    GrpTpl.bind(grp_id, tpl_id, g.user.name)
    return jsonify(msg='')
