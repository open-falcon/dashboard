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


__author__ = 'Ulric Qin'
from flask import jsonify, render_template, request, g
from flask.ext.babel import gettext
from rrd import app
from rrd.model.portal.host_group import HostGroup
from rrd.model.portal.cluster import Cluster
from rrd.utils.params import required_chk


@app.route('/portal/group/<group_id>/cluster')
def cluster_list_get(group_id):
    group_id = int(group_id)

    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group %s' % group_id)

    clusters = Cluster.select_vs(where='grp_id = %s', params=[group_id])
    return render_template('portal/cluster/list.html', **locals())


@app.route('/portal/group/<group_id>/cluster/creator', methods=['GET'])
def cluster_creator_get(group_id):
    group_id = int(group_id)
    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group %s' % group_id)

    return render_template('portal/cluster/creator.html', **locals())


@app.route('/portal/group/<group_id>/cluster/creator', methods=['POST'])
def cluster_node_post(group_id):
    group_id = int(group_id)
    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group %s' % group_id)

    numerator = request.form['numerator'].strip()
    denominator = request.form['denominator'].strip()
    endpoint = request.form['endpoint'].strip()
    metric = request.form['metric'].strip()
    tags = request.form['tags'].strip()
    ds_type = 'GAUGE'
    step = request.form['step'].strip()

    msg = required_chk({
        'numerator': numerator,
        'denominator': denominator,
        'endpoint': endpoint,
        'metric': metric,
        'ds_type': ds_type,
        'step': step,
    })

    if msg:
        return jsonify(msg=msg)

    if Cluster.exists('endpoint=%s and metric=%s and tags=%s', [endpoint, metric, tags]):
        return jsonify(msg='%s/%s/%s is already existent' % (endpoint, metric, tags))

    last_id = Cluster.insert({
        'grp_id': group_id,
        'numerator': numerator,
        'denominator': denominator,
        'endpoint': endpoint,
        'metric': metric,
        'tags': tags,
        'ds_type': ds_type,
        'step': step,
        'creator': g.user.name,
    })

    if last_id > 0:
        return jsonify(msg='')
    else:
        return jsonify(msg='occur error')


@app.route('/portal/cluster/edit/<cluster_id>', methods=['GET'])
def cluster_edit_get(cluster_id):
    cluster_id = int(cluster_id)
    cluster = Cluster.get(cluster_id)
    op = gettext('edit')
    return render_template('portal/cluster/edit.html', **locals())


@app.route('/portal/cluster/clone/<cluster_id>', methods=['GET'])
def cluster_clone_get(cluster_id):
    cluster_id = int(cluster_id)
    cluster = Cluster.get(cluster_id)
    # for clone
    cluster_id = 0
    op = gettext('clone')
    return render_template('portal/cluster/edit.html', **locals())


@app.route('/portal/cluster/delete/<cluster_id>', methods=['POST'])
def cluster_delete_post(cluster_id):
    cluster_id = int(cluster_id)
    Cluster.delete_one(cluster_id)
    return jsonify(msg='')


@app.route('/portal/cluster/edit/<cluster_id>', methods=['POST'])
def cluster_edit_post(cluster_id):
    cluster_id = int(cluster_id)
    numerator = request.form['numerator'].strip()
    denominator = request.form['denominator'].strip()
    endpoint = request.form['endpoint'].strip()
    metric = request.form['metric'].strip()
    tags = request.form['tags'].strip()
    ds_type = 'GAUGE'
    step = request.form['step'].strip()
    grp_id = request.form['grp_id'].strip()
    if cluster_id:
        # edit
        if Cluster.exists('endpoint=%s and metric=%s and tags=%s and id<>%s', [endpoint, metric, tags, cluster_id]):
            return jsonify(msg='%s/%s/%s has already existent' % (endpoint, metric, tags))
        Cluster.update_dict({
            'numerator': numerator,
            'denominator': denominator,
            'endpoint': endpoint,
            'metric': metric,
            'tags': tags,
            'ds_type': ds_type,
            'step': step,
        }, 'id=%s', [cluster_id])
    else:
        # clone
        last_id = Cluster.insert({
            'numerator': numerator,
            'denominator': denominator,
            'endpoint': endpoint,
            'metric': metric,
            'tags': tags,
            'ds_type': ds_type,
            'step': step,
            'creator': g.user.name,
            'grp_id': grp_id,
        })

        if last_id <= 0:
            return jsonify(msg='occur error')

    return jsonify(msg='')
