## Introduction

dashboard是提供给用户，以图表的方式查看push上来的数据


## Clone

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

    $ mysql -h localhost -u root -p < ../scripts/db_schema/dashboard-db-schema.sql
    $ mysql -h localhost -u root -p < ../scripts/db_schema/graph-db-schema.sql

    ## default mysql user is root, default passwd is ""
    ## change mysql info in rrd/config.py if necessary


## Start

    $ ./env/bin/python wsgi.py

    --> goto http://127.0.0.1:8081


## Run with gunicorn

    $ bash control start

    --> goto http://127.0.0.1:8081


## Stop gunicorn

    $ bash control stop

## Check log

    $ bash control tail
