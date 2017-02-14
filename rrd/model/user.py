#-*- coding:utf-8 -*-
class User(object):
    def __init__(self, id):
        self.name = None
        self.session_id = None
    
    def __repr__(self):
        return "<User name=%s, session_id=%s>" \
                % (self.name, self.session_id)
    __str__ = __repr__

    @classmethod
    def get(cls, name):
        return None
