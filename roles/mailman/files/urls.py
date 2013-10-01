# -*- coding: utf-8 -*-

import hyperkitty
import postorius

from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Import mailman urls and set urlpatterns if you want to hook
# mailman_django into an existing django site. 
# Otherwise set ROOT_URLCONF in settings.py to
# `mailman_django.urls`.
# from mailman_django import urls as mailman_urls

urlpatterns = patterns('',
    #url(r'^$', 'postorius.views.list_index'),
    url(r'^admin/', include('postorius.urls')),
    url(r'^$', 'hyperkitty.views.pages.index'),
    url(r'^archives/', include('hyperkitty.urls')),
    url(r'', include('social_auth.urls')),
)
