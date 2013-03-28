import __main__
if hasattr(__main__, '__requires__'):
    if isinstance(__main__.__requires__, basestring):
        __main__.__requires__ = [__main__.__requires__]
else:
    __main__.__requires__ = []
__main__.__requires__.append('Trac')

import os

os.environ['TRAC_ENV_PARENT_DIR'] = '/srv/www/trac/projects'
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/trac'

import trac.web.main
application = trac.web.main.dispatch_request
