#!/usr/bin/env python3

import os
import logging

from app import app

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.debug('Ce message ne sera pas affiché')
    logging.info('Ce message sera affiché')

    app.run(debug=bool(int(os.environ.get('DEBUG'))),host='0.0.0.0')
