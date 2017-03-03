#-*- coding:utf-8 -*-
class Team(object):
    def __init__(self, id, name, resume, creator, users=[]):
        self.id = id
        self.name = name
        self.resume = resume
        self.creator = creator
        self.users = users

    def __repr__(self):
        return "<Team id=%s, name=%s>" % (self.id, self.name)
    __str__ = __repr__
