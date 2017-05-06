# -*- coding:utf-8 -*-
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
