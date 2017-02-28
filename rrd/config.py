#-*-coding:utf8-*-
import os

#-- app config --
DEBUG = True
SECRET_KEY = "secret-key"
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30
SITE_COOKIE = "open-falcon-ck"

BASE_DIR = "/home/work/open-falcon/dashboard/"
LOG_PATH = os.path.join(BASE_DIR,"log/")

#-- API -- 
API_ADDR = "http://127.0.0.1:8080/api/v1"

try:
    from rrd.local_config import *
except:
    pass
