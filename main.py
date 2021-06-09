#!/usr/bin/env python3

from app import app
import os

if __name__ == '__main__':
    # for key in os.environ:
    #     print(key, "---->", os.environ[key])
    # print(os.environ['PORT'])
    app.run(debug=True)
