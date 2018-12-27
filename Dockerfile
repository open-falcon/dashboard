FROM python:2.7-alpine3.7
USER root
ENV prefix=/open-falcon
ENV workdir=$prefix/dashboard

RUN apk add --no-cache \
    ca-certificates bash git g++ perl make \
    py-mysqldb \
    py-pyldap

RUN mkdir -p $prefix

ENV PYTHONPATH "${PYTHONPATH}:/usr/lib/python2.7/site-packages/"
WORKDIR $workdir
ADD ./ ./
RUN pip install \
    Flask==0.10.1 \
    Flask-Babel==0.9 \
    Jinja2==2.7.2 \
    Werkzeug==0.9.4 \
    gunicorn==19.9.0 \
    python-dateutil==2.2 \
    requests==2.3.0

ENTRYPOINT ["/bin/sh", "-c"]
