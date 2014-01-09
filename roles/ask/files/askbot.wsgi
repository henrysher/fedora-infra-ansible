#!/usr/bin/python
import os
import sys
sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Here we have to trick askbot into thinking its using ssl so it
# produces the correct URLs for openid/auth stuff (mostly for stg).
os.environ['HTTPS'] = "on"
def is_secure(self):
    return True
import django.core.handlers.wsgi
django.core.handlers.wsgi.WSGIRequest.is_secure = is_secure

application = django.core.handlers.wsgi.WSGIHandler()
