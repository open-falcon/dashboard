# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'
from rrd import app
from flask import jsonify, render_template, request, g
from rrd.model.portal.host_group import HostGroup
from rrd.model.portal.plugin_dir import PluginDir


@app.route('/group/<group_id>/plugins')
def plugin_list_get(group_id):
    group_id = int(group_id)

    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group %s' % group_id)

    plugins = PluginDir.select_vs(where='grp_id = %s', params=[group_id])
    return render_template('portal/plugin/list.html', group=group, plugins=plugins)


@app.route('/plugin/bind', methods=['POST'])
def plugin_bind_post():
    group_id = int(request.form['group_id'].strip())
    plugin_dir = request.form['plugin_dir'].strip()
    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group %s' % group_id)

    PluginDir.insert({'grp_id': group_id, 'dir': plugin_dir, 'create_user': g.user.name})
    return jsonify(msg='')


@app.route('/plugin/delete/<plugin_id>')
def plugin_delete_get(plugin_id):
    plugin_id = int(plugin_id)
    plugin = PluginDir.read(where='id = %s', params=[plugin_id])
    if not plugin:
        return jsonify(msg='no such plugin dir %s' % plugin_id)
    PluginDir.delete_one(plugin_id)
    return jsonify(msg='')

