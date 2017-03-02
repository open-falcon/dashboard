#-*- coding:utf-8 -*-
class UserToken(object):
    def __init__(self, name, sig):
        self.name = name
        self.sig = sig
    
    def __repr__(self):
        return "<User name=%s, sig=%s>"  % (self.name, self.sig)
    __str__ = __repr__

class User(object):
    def __init__(self, id, name, cnname, email, phone, im, qq, role):
        self.id = id
        self.name = name
        self.cnname = cnname
        self.email = email
        self.phone = phone
        self.im = im
        self.qq = qq
        self.role = role

    def __repr__(self):
        return "<UserProfile id=%s, name=%s, cnname=%s>" \
                % (self.id, self.name, self.cnname)
    __str__ = __repr__

    def is_root(self):
        return str(self.role) == "2"

    def is_admin(self):
        return str(self.role) == "1"
