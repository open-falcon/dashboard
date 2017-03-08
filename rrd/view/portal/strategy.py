# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'
from rrd import app
from flask import request, jsonify
from rrd.model.portal.strategy import Strategy


@app.route('/portal/strategy/update', methods=['POST'])
def strategy_update_post():
    sid = request.form['sid'].strip()
    metric = request.form['metric'].strip()
    tags = request.form['tags'].strip()
    max_step = request.form['max_step'].strip()
    priority = request.form['priority'].strip()
    note = request.form['note'].strip()
    func = request.form['func'].strip()
    op = request.form['op'].strip()
    right_value = request.form['right_value'].strip()
    run_begin = request.form['run_begin'].strip()
    run_end = request.form['run_end'].strip()
    tpl_id = request.form['tpl_id'].strip()

    if not metric:
        return jsonify(msg='metric is blank')

    if metric == 'net.port.listen' and '=' not in tags:
        return jsonify(msg='if metric is net.port.listen, tags should like port=22')

    if sid:
        # update
        Strategy.update_dict(
            {
                'metric': metric,
                'tags': tags,
                'max_step': max_step,
                'priority': priority,
                'func': func,
                'op': op,
                'right_value': right_value,
                'note': note,
                'run_begin': run_begin,
                'run_end': run_end
            },
            'id=%s',
            [sid]
        )
        return jsonify(msg='')

    # insert
    Strategy.insert(
        {
            'metric': metric,
            'tags': tags,
            'max_step': max_step,
            'priority': priority,
            'func': func,
            'op': op,
            'right_value': right_value,
            'note': note,
            'run_begin': run_begin,
            'run_end': run_end,
            'tpl_id': tpl_id
        }
    )
    return jsonify(msg='')


@app.route('/portal/strategy/<sid>')
def strategy_get(sid):
    sid = int(sid)
    s = Strategy.get(sid)
    if not s:
        return jsonify(msg='no such strategy')

    return jsonify(msg='', data=s.to_json())


@app.route('/portal/strategy/delete/<sid>')
def strategy_delete_get(sid):
    sid = int(sid)
    s = Strategy.get(sid)
    if not s:
        return jsonify(msg='no such strategy')

    Strategy.delete_one(sid)

    return jsonify(msg='')
