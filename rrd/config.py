#-*-coding:utf8-*-
# app config
import os
LOG_LEVEL = os.environ.get("LOG_LEVEL",'DEBUG')
SECRET_KEY = os.environ.get("SECRET_KEY","secret-key")
PERMANENT_SESSION_LIFETIME = os.environ.get("PERMANENT_SESSION_LIFETIME",3600 * 24 * 30)
SITE_COOKIE = os.environ.get("SITE_COOKIE","open-falcon-ck")

# Falcon+ API
API_ADDR = os.environ.get("API_ADDR","http://127.0.0.1:8080/api/v1")

# portal database
# TODO: read from api instead of db
PORTAL_DB_HOST = os.environ.get("PORTAL_DB_HOST","127.0.0.1")
PORTAL_DB_PORT = int(os.environ.get("PORTAL_DB_PORT",3306))
PORTAL_DB_USER = os.environ.get("PORTAL_DB_USER","root")
PORTAL_DB_PASS = os.environ.get("PORTAL_DB_PASS","")
PORTAL_DB_NAME = os.environ.get("PORTAL_DB_NAME","falcon_portal")

# alarm database
# TODO: read from api instead of db
ALARM_DB_HOST = os.environ.get("ALARM_DB_HOST","127.0.0.1")
ALARM_DB_PORT = int(os.environ.get("ALARM_DB_PORT",3306))
ALARM_DB_USER = os.environ.get("ALARM_DB_USER","root")
ALARM_DB_PASS = os.environ.get("ALARM_DB_PASS","")
ALARM_DB_NAME = os.environ.get("ALARM_DB_NAME","alarms")

# ldap config
LDAP_ENABLED = os.environ.get("LDAP_ENABLED",False)
LDAP_SERVER = os.environ.get("LDAP_SERVER","ldap.forumsys.com:389")
LDAP_BASE_DN = os.environ.get("LDAP_BASE_DN","dc=example,dc=com")
LDAP_BINDDN_FMT = os.environ.get("LDAP_BINDDN_FMT","uid=%s,dc=example,dc=com")
LDAP_SEARCH_FMT = os.environ.get("LDAP_SEARCH_FMT","uid=%s")
LDAP_ATTRS = ["cn","mail","telephoneNumber"]
LDAP_TLS_START_TLS = False
LDAP_TLS_CACERTDIR = ""
LDAP_TLS_CACERTFILE = "/etc/openldap/certs/ca.crt"
LDAP_TLS_CERTFILE = ""
LDAP_TLS_KEYFILE = ""
LDAP_TLS_REQUIRE_CERT = True
LDAP_TLS_CIPHER_SUITE = ""

# i18n
BABEL_DEFAULT_LOCALE   = 'zh_CN'
BABEL_DEFAULT_TIMEZONE = 'Asia/Shanghai'
# aviliable translations
LANGUAGES   = {
    'en':  'English',
    'zh_CN':  'Chinese-Simplified',
}

# portal site config
MAINTAINERS = ['root']
CONTACT = 'root@open-falcon.org'

try:
    from rrd.local_config import *
except:
    print "[warning] no local config file"
