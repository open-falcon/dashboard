#-*-coding:utf8-*-
# app config
LOG_LEVEL = 'DEBUG'
SECRET_KEY = "secret-key"
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30
SITE_COOKIE = "open-falcon-ck"

# Falcon+ API
API_ADDR = "http://127.0.0.1:8080/api/v1"

# portal database
# TODO: read from api instead of db
PORTAL_DB_HOST = "127.0.0.1"
PORTAL_DB_PORT = 3306
PORTAL_DB_USER = "root"
PORTAL_DB_PASS = ""
PORTAL_DB_NAME = "falcon_portal"

# alarm database
# TODO: read from api instead of db
ALARM_DB_HOST = "127.0.0.1"
ALARM_DB_PORT = 3306
ALARM_DB_USER = "root"
ALARM_DB_PASS = ""
ALARM_DB_NAME = "alarms"

# ldap config
LDAP_ENABLED = False
LDAP_SERVER = "ldap.forumsys.com:389"
LDAP_BASE_DN = "dc=example,dc=com"
LDAP_BINDDN_FMT = "uid=%s,dc=example,dc=com"
LDAP_SEARCH_FMT = "uid=%s"
LDAP_ATTRS = ["cn","mail","telephoneNumber"]

# portal site config
MAINTAINERS = ['root']
CONTACT = 'root@open-falcon.org'

try:
    from rrd.local_config import *
except:
    print "[warning] no local config file"
