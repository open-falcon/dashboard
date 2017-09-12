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
from flask import request, g, render_template, jsonify
from rrd.model.portal.expression import Expression
from rrd.model.portal.action import Action
from rrd.utils.params import required_chk

@app.route('/portal/expression')
def expressions_get():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 6))
    query = request.args.get('q', '').strip()
    mine = request.args.get('mine', '1')
    me = g.user.name if mine == '1' else None
    vs, total = Expression.query(page, limit, query, me)
    for v in vs:
        v.action = Action.get(v.action_id)
    return render_template(
        'portal/expression/list.html',
        data={
            'vs': vs,
            'total': total,
            'query': query,
            'limit': limit,
            'page': page,
            'mine': mine,
        }
    )


@app.route('/portal/expression/delete/<expression_id>')
def expression_delete_get(expression_id):
    expression_id = int(expression_id)
    Expression.delete_one(expression_id)
    return jsonify(msg='')


@app.route('/portal/expression/add')
def expression_add_get():
    a = None
    o = Expression.get(int(request.args.get('id', '0').strip()))
    if o:
        a = Action.get(o.action_id)
    return render_template('portal/expression/add.html',
                           data={'action': a, 'expression': o})


@app.route('/portal/expression/update', methods=['POST'])
def expression_update_post():
    expression_id = request.form['expression_id'].strip()
    expression = request.form['expression'].strip()
    func = request.form['func'].strip()
    op = request.form['op'].strip()
    right_value = request.form['right_value'].strip()
    uic_groups = request.form['uic'].strip()
    max_step = request.form['max_step'].strip()
    priority = int(request.form['priority'].strip())
    note = request.form['note'].strip()
    url = request.form['url'].strip()
    callback = request.form['callback'].strip()
    before_callback_sms = request.form['before_callback_sms']
    before_callback_mail = request.form['before_callback_mail']
    after_callback_sms = request.form['after_callback_sms']
    after_callback_mail = request.form['after_callback_mail']

    msg = required_chk({
        'expression': expression,
        'func': func,
        'op': op,
        'right_value': right_value,
    })

    if msg:
        return jsonify(msg=msg)

    if not max_step:
        max_step = 3

    if not priority:
        priority = 0

    return jsonify(msg=Expression.save_or_update(
        expression_id,
        expression,
        func,
        op,
        right_value,
        uic_groups,
        max_step,
        priority,
        note,
        url,
        callback,
        before_callback_sms,
        before_callback_mail,
        after_callback_sms,
        after_callback_mail,
        g.user.name,
    ))


@app.route('/portal/expression/pause')
def expression_pause_get():
    expression_id = request.args.get("id", '')
    pause = request.args.get('pause', '')
    if not expression_id:
        return jsonify(msg='id is blank')

    if not pause:
        return jsonify(msg='pause is blank')

    e = Expression.get(expression_id)
    if not e:
        return jsonify('no such expression %s' % expression_id)

    Expression.update_dict({'pause': pause}, 'id=%s', [expression_id])
    return jsonify(msg='')


@app.route('/portal/expression/view/<eid>')
def expression_view_get(eid):
    eid = int(eid)
    a = None
    o = Expression.get(eid)
    if o:
        a = Action.get(o.action_id)
    else:
        return 'no such expression'
    return render_template('portal/expression/view.html', data={'action': a, 'expression': o})
