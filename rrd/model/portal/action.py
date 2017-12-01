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
from .bean import Bean

class Action(Bean):
    _tbl = 'action'
    _cols = 'id, uic, url, callback, ' \
            'before_callback_sms, before_callback_mail, after_callback_sms, after_callback_mail'

    def __init__(self, _id, uic, url, callback,
                 before_callback_sms, before_callback_mail, after_callback_sms, after_callback_mail):
        self.id = _id
        self.uic = uic  ##teams_name
        self.url = url
        self.callback = callback
        self.before_callback_sms = before_callback_sms
        self.before_callback_mail = before_callback_mail
        self.after_callback_sms = after_callback_sms
        self.after_callback_mail = after_callback_mail

    def html(self):
        if self.url:
            return 'curl %s' % self.url
        if self.uic:
            return 'alarm to %s' % self.uic_href()
        return 'do nothing'

    def uic_href(self):
        if not self.uic:
            return ''
        arr = self.uic.split(',')
        arr = ['<a target="_blank" href="/team/%s/users">%s</a>' % (team, team)
               for team in arr]
        return ' '.join(arr)

    def to_json(self):
        return {
            'id': self.id,
            'uic': self.uic,
            'url': self.url,
            'callback': self.callback,
            'before_callback_sms': self.before_callback_sms,
            'before_callback_mail': self.before_callback_mail,
            'after_callback_sms': self.after_callback_sms,
            'after_callback_mail': self.after_callback_mail,
        }
