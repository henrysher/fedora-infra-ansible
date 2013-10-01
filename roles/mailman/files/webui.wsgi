"""
WSGI config for hyperkitty_standalone project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
import site


## For some unknown reason, sometimes mod_wsgi fails to set the python paths to
## the virtualenv, with the 'python-path' option. You can do it here too.
##
## Remember original sys.path.
#prev_sys_path = list(sys.path)
## Add here, for the settings module
#site.addsitedir(os.path.abspath(os.path.dirname(__file__)))
## Add the virtualenv
#venv = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'lib', 'python2.6', 'site-packages')
#site.addsitedir(venv)
# Reorder sys.path so new directories at the front.
#new_sys_path = []
#for item in list(sys.path):
#    if item not in prev_sys_path:
#        new_sys_path.append(item)
#        sys.path.remove(item)
#        sys.path[:0] = new_sys_path

site.addsitedir(os.path.abspath(os.path.dirname(__file__)))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
