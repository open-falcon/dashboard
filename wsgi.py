#-*- coding:utf-8 -*-
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
activate_this = '%s/env/bin/activate_this.py' % base_dir
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, base_dir)

from rrd import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
