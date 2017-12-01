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
from flask import g, render_template, request, jsonify
from rrd.model.portal.template import Template
from rrd.model.portal.strategy import Strategy
from rrd.model.portal.action import Action
from rrd.model.portal.grp_tpl import GrpTpl
from rrd.model.portal.host_group import HostGroup

from rrd.utils.logger import logging
log = logging.getLogger(__file__)

@app.route('/portal/template')
def templates_get():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 10))
    query = request.args.get('q', '').strip()
    mine = request.args.get('mine', '1')
    me = g.user.name if mine == '1' else None
    vs, total = Template.query(page, limit, query, me)
    for v in vs:
        v.parent = Template.get(v.parent_id)
    return render_template(
        'portal/template/list.html',
        data={
            'vs': vs,
            'total': total,
            'query': query,
            'limit': limit,
            'page': page,
            'mine': mine,
        }
    )


@app.route('/portal/template/create', methods=['POST'])
def template_create_post():
    name = request.form['name'].strip()
    if not name:
        return jsonify(msg='name is blank')

    if Template.read('tpl_name=%s', [name]):
        return jsonify(msg='name already existent')

    tpl_id = Template.insert({'tpl_name': name, 'create_user': g.user.name})
    if tpl_id:
        return jsonify(msg='', id=tpl_id)

    return jsonify(msg='create fail')


@app.route('/portal/template/update/<tpl_id>')
def template_update_get(tpl_id):
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    if not t:
        return jsonify(msg='no such template')

    t.parent = Template.get(t.parent_id)
    ss = Strategy.select_vs(where='tpl_id = %s', params=[tpl_id], order='metric')
    t.action = Action.get(t.action_id)
    log.debug(t)
    return render_template('portal/template/update.html', data={'tpl': t, 'ss': ss})


@app.route('/portal/template/binds/<tpl_id>')
def template_binds_get(tpl_id):
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    if not t:
        return jsonify(msg='no such template')

    groups = GrpTpl.grp_list(tpl_id)
    return render_template('portal/template/groups.html', data={
        "gs": groups,
        "tpl": t,
    })


@app.route('/portal/template/unbind/group')
def template_unbind_group_get():
    tpl_id = request.args.get('tpl_id', '')
    grp_id = request.args.get('grp_id', '')
    if not tpl_id:
        return jsonify(msg="tpl_id is blank")

    if not grp_id:
        return jsonify(msg="grp_id is blank")

    GrpTpl.unbind(grp_id, tpl_id)
    return jsonify(msg='')


@app.route('/portal/template/unbind/node')
def template_unbind_grp_name_get():
    tpl_id = request.args.get('tpl_id', '')
    if not tpl_id:
        return jsonify(msg="tpl_id is blank")

    grp_name = request.args.get('grp_name', '')
    if not grp_name:
        return jsonify(msg='grp_name is blank')

    hg = HostGroup.read('grp_name=%s', [grp_name])
    if not hg:
        return jsonify(msg='no such host group')

    GrpTpl.unbind(hg.id, tpl_id)
    return jsonify(msg='')


@app.route('/portal/template/bind/node', methods=['POST'])
def template_bind_node_post():
    node = request.form['node'].strip()
    tpl_id = request.form['tpl_id'].strip()
    if not node:
        return jsonify(msg='node is blank')

    if not tpl_id:
        return jsonify(msg='tpl id is blank')

    hg = HostGroup.read('grp_name=%s', [node])
    if not hg:
        return jsonify(msg='no such node')

    GrpTpl.bind(hg.id, tpl_id, g.user.name)
    return jsonify(msg="")


@app.route('/portal/template/view/<tpl_id>')
def template_view_get(tpl_id):
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    if not t:
        return jsonify(msg='no such template')

    t.parent = Template.get(t.parent_id)
    ss = Strategy.select_vs(where='tpl_id = %s', params=[tpl_id], order='metric')
    t.action = Action.get(t.action_id)
    return render_template('portal/template/view.html', data={'tpl': t, 'ss': ss})


@app.route('/portal/template/fork/<tpl_id>')
def template_fork_get(tpl_id):
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    if not t:
        return jsonify(msg='no such template')

    new_id = t.fork(g.user.name)
    if new_id == -1:
        return jsonify(msg='name[copy_of_%s] has already existent' % t.tpl_name)
    return jsonify(msg='', id=new_id)


@app.route('/portal/template/help')
def template_help_get():
    contact = app.config['CONTACT']
    return render_template('portal/template/help.html', contact=contact)


@app.route('/portal/template/delete/<tpl_id>')
def template_delete_get(tpl_id):
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    if not t:
        return jsonify(msg='no such template')

    if not t.writable(g.user):
        return jsonify(msg='no permission')

    Template.delete_one(tpl_id)
    action_id = t.action_id
    if action_id:
        Action.delete_one(action_id)

    Strategy.delete('tpl_id = %s', [tpl_id])

    GrpTpl.unbind_tpl(tpl_id)
    return jsonify(msg='')


@app.route('/portal/template/rename/<tpl_id>', methods=['POST'])
def template_rename_post(tpl_id):
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    if not t:
        return jsonify(msg='no such template')

    name = request.form['name'].strip()
    parent_id = request.form.get('parent_id', '')
    if not parent_id:
        parent_id = 0

    Template.update_dict({'tpl_name': name, 'parent_id': parent_id}, 'id=%s', [tpl_id])
    return jsonify(msg='')


@app.route('/portal/template/action/update/<tpl_id>', methods=['POST'])
def template_action_update_post(tpl_id):
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    if not t:
        return jsonify(msg='no such template')

    uic = request.form['uic'].strip()
    url = request.form['url'].strip()
    callback = request.form['callback'].strip()
    before_callback_sms = request.form['before_callback_sms'].strip()
    before_callback_mail = request.form['before_callback_mail'].strip()
    after_callback_sms = request.form['after_callback_sms'].strip()
    after_callback_mail = request.form['after_callback_mail'].strip()

    if t.action_id > 0:
        # update
        Action.update_dict(
            {
                'uic': uic,
                'url': url,
                'callback': callback,
                'before_callback_sms': before_callback_sms,
                'before_callback_mail': before_callback_mail,
                'after_callback_sms': after_callback_sms,
                'after_callback_mail': after_callback_mail
            },
            'id=%s',
            [t.action_id]
        )
    else:
        # insert
        action_id = Action.insert({
            'uic': uic,
            'url': url,
            'callback': callback,
            'before_callback_sms': before_callback_sms,
            'before_callback_mail': before_callback_mail,
            'after_callback_sms': after_callback_sms,
            'after_callback_mail': after_callback_mail
        })
        if action_id <= 0:
            return jsonify(msg='insert action fail')

        Template.update_dict({'action_id': action_id}, 'id=%s', [t.id])
    return jsonify(msg='')
