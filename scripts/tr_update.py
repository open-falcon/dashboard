#!env/bin/python
import os
import sys
if sys.platform == 'win32':
    pybabel = 'env\\Scripts\\pybabel'
else:
    pybabel = 'env/bin/pybabel'
os.system(pybabel + ' extract -F babel.cfg -k lazy_gettext -o messages.pot rrd')
os.system(pybabel + ' update -i messages.pot -d rrd/translations')
os.unlink('messages.pot')
