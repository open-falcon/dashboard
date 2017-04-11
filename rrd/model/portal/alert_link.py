#-*- coding:utf-8 -*-
from .bean import Bean

class AlertLink(Bean):
    _tbl = 'alert_link'
    _cols = 'id, path, content'

    def __init__(self, _id, path, content):
        self.id = _id
        self.path = path
        self.content = content
