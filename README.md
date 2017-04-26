## Introduction
dashboard是Open-Falcon统一的front-end组件，提供以下功能：

- 自定义仪表盘：dashboard、screen
- 告警配置管理：hostgroup、template 
- 历史告警信息管理： alarm-dashboard（告警列表、未恢复告警、删除告警信息）
- 用户组和通讯录：teams、users
- 告警合并管理：alarm-links
- 用户注册、登录和权限管理：login、logout、register、ldap_login

Open-Falcon 官网为：[http://open-falcon.org](http://open-falcon.org)

## Demo site
- TODO

## Clone & Prepare
```
export HOME=/home/work/

mkdir -p $HOME/open-falcon/
cd $HOME/open-falcon && git clone https://github.com/open-falcon/dashboard.git
cd dashboard;

```

## Install dependency
```
yum install -y python-virtualenv
yum install -y python-devel
yum install -y openldap-devel
yum install -y mysql-devel
yum groupinstall "Development tools"

cd $HOME/open-falcon/dashboard/
virtualenv ./env

./env/bin/pip install -r pip_requirements.txt -i http://pypi.douban.com/simple

```

## Init database
```
    cd /tmp/ && git clone https://github.com/open-falcon/falcon-plus.git 
    cd /tmp/falcon-plus/scripts/mysql/db_schema/
    mysql -h 127.0.0.1 -u root -p < uic-db-schema.sql
    mysql -h 127.0.0.1 -u root -p < portal-db-schema.sql
    mysql -h 127.0.0.1 -u root -p < graph-db-schema.sql
    mysql -h 127.0.0.1 -u root -p < dashboard-db-schema.sql
    mysql -h 127.0.0.1 -u root -p < alarms-db-schema.sql
    rm -rf /tmp/falcon-plus/
```

**if you are upgrading from v0.1 to current version v0.2.0,then**

    mysql -h 127.0.0.1 -u root -p < alarms-db-schema.sql
    
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


## Screenshots

<img src="screenshots/dashboard.jpeg" width=500px />
<img src="screenshots/alarm-dashboard-case.jpeg" width=500px />
<img src="screenshots/alarm-dashboard-case-events.jpeg" width=500px />
 
## Mailing lists

- [openfalcon-users](https://groups.google.com/forum/#!forum/openfalcon-users) – for discussions around openfalcon usage and community support
- [openfalcon-developers](https://groups.google.com/forum/#!forum/openfalcon-developers) – for discussions around openfalcon development

## Issue tracker

We are using the [github issue tracker](https://github.com/open-falcon/falcon-plus/issues) for the various Open-Falcon repositories to fix bugs and features request. If you need support, please send your questions to the [openfalcon-users](https://groups.google.com/forum/#!forum/openfalcon-users) mailing list rather than filing a GitHub issue.

Please do not ask individual project members for support. Use the channels above instead, where the whole community can help you and benefit from the solutions provided. If community support is insufficient for your situation, please refer to the Commercial Support section below.

## Contributing
We welcome community contributions! Open-Falcon uses GitHub to manage reviews of pull requests.

If you have a trivial fix or improvement, go ahead and create a pull request, addressing (with `@...`) the maintainer of this repository in the description of the pull request.

If you plan to do something more involved, first discuss your ideas on our mailing list. This will avoid unnecessary work and surely give you and us a good deal of inspiration.

## Acknowledgements

Open-Falcon was initially started by Xiaomi and we would also like to acknowledge early contributions by engineers from these companies.

[Wei Lai](https://github.com/laiwei) is the founder of Open-Falcon software and community. 

The Open-Falcon logo and website were contributed by Cepave Design Team.
