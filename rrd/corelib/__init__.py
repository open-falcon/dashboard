#-*- coding:utf-8 -*-
from rrd import config 
from rrd.utils import randbytes

def auth_user_from_session(session_):
    user = None
    if config.SITE_COOKIE in session_:
        cookies = session_[config.SITE_COOKIE]
        user_id, session_id = cookies.split(":")

    return user 

def set_user_cookie(user, session_):
    if not user:
        return None
    session_id = user.session_id if user.session_id else randbytes(8)
    #user.update_session(session_id)
    session_[config.SITE_COOKIE] = "%s:%s" % (user.id, session_id)

def logout_user(user):
    if not user:
        return 
    #user.clear_session()

