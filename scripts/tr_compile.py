#!env/bin/python
import os
import sys
if sys.platform == 'win32':
    pybabel = 'env\\Scripts\\pybabel'
else:
    pybabel = 'env/bin/pybabel'
os.system(pybabel + ' compile -d rrd/translations')
