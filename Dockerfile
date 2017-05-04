FROM centos:7.3.1611

RUN yum clean all && yum install -y epel-release && yum -y update && \
yum install -y git python-virtualenv python-devel openldap-devel mysql-devel && \
yum groupinstall -y "Development tools"

RUN export HOME=/home/work/ && mkdir -p $HOME/open-falcon/dashboard && cd $HOME/open-falcon/dashboard
WORKDIR /home/work/open-falcon/dashboard
ADD ./ ./
RUN virtualenv ./env && ./env/bin/pip install -r pip_requirements.txt -i http://pypi.douban.com/simple

ADD ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
