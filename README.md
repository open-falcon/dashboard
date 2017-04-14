## Introduction
dashboard是Open-Falcon统一的front-end组件，提供以下功能：

- 自定义仪表盘：dashboard、screen
- 告警配置管理：hostgroup、template 
- 历史告警信息管理： alarm-dashboard（告警列表、未恢复告警、删除告警信息）
- 用户组和通讯录：teams、users
- 告警合并管理：alarm-links
- 用户注册、登录和权限管理：login、logout、register、ldap_login


## Clone & Prepare

    $ export HOME=/home/work/

    $ mkdir -p $HOME/open-falcon/
    $ cd $HOME/open-falcon && git clone https://github.com/open-falcon/dashboard.git
    $ cd dashboard;

## Install dependency

    # yum install -y python-virtualenv

    $ cd $HOME/open-falcon/dashboard/
    $ virtualenv ./env

    $ ./env/bin/pip install -r pip_requirements.txt -i http://pypi.douban.com/simple


## Init database

    $ cd /tmp/ && git clone https://github.com/open-falcon/falcon-plus.git 
    $ cd /tmp/falcon-plus/scripts/mysql/db_schema/
    $ mysql -h 127.0.0.1 -u root -p < alarms-db-schema.sql
    $ mysql -h 127.0.0.1 -u root -p < portal-db-schema.sql

**if you are upgrading from v0.1 to current version v0.2.0,then**

    $  mysql -h 127.0.0.1 -u root -p < alarms-db-schema.sql
    
## Configure
    dashboard config file is 'rrd/config.py', change it if necessary.
   
    ## set API_ADDR to your falcon-plus api modules addr, default value as bellow:
    API_ADDR = "http://127.0.0.1:8080/api/v1" 

    ## set PORTAL_DB_* if necessary, default mysql user is root, default passwd is ""
    ## set ALARM_DB_* if necessary, default mysql user is root, default passwd is ""

## Start in debug mode

    $ ./env/bin/python wsgi.py

    --> goto http://127.0.0.1:8081


## Run with gunicorn in production mode

    $ bash control start

    --> goto http://127.0.0.1:8081


## Stop gunicorn

    $ bash control stop

## Check log

    $ bash control tail
