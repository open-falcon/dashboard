# -*- coding:utf-8 -*-
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
