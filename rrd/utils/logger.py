#-*- coding:utf-8 -*-
from rrd import config
import logging

logging.basicConfig(level=config.LOG_LEVEL,
        format='%(asctime)s %(filename)s[%(lineno)d] [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=config.LOG_FILE,
        filemode='a+')

