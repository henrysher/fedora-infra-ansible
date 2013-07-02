import sys
sys.stdout = sys.stderr

import __main__
__main__.__requires__ = __requires__ = ["tahrir", "sqlalchemy>=0.7"];
import pkg_resources
pkg_resources.require(__requires__)

import os
os.environ['PYTHON_EGG_CACHE'] = '/var/www/.python-eggs'

from pyramid.paster import get_app, setup_logging
ini_path = '/etc/tahrir/tahrir.ini'
setup_logging(ini_path)

pyramid_app = get_app(ini_path, 'main')

def reverse_proxy_handler(environ, start_response):
    environ['HTTP_HOST'] = environ['HTTP_X_FORWARDED_HOST']
    environ['wsgi.url_scheme'] = 'https'
    return pyramid_app(environ, start_response)

application = reverse_proxy_handler
