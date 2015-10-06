from .common import *

MEDIA_URL = "http://{{ inventory_hostname }}/media/"
STATIC_URL = "http://{{ inventory_hostname }}/static/"
ADMIN_MEDIA_PREFIX = "http://{{ inventory_hostname }}/static/admin/"
SITES["front"]["scheme"] = "http"
SITES["front"]["domain"] = "{{ inventory_hostname }}"

SECRET_KEY = "{{ taiga_secret_key }}"

DEBUG = False
TEMPLATE_DEBUG = False
PUBLIC_REGISTER_ENABLED = True

DEFAULT_FROM_EMAIL = "nobody@fedoraproject.org"
SERVER_EMAIL = DEFAULT_FROM_EMAIL

INSTALLED_APPS += ["taiga_contrib_fas_openid_auth"]
# We monkey patch the rest_framework exception handler to allow us to do
# the 303 redirects that we need to do for openid to finish.
REST_FRAMEWORK['EXCEPTION_HANDLER'] = "taiga_contrib_fas_openid_auth.services.exception_handler"

## Uncomment all this stuff to get the async celery stuff working.
## It is not necessary.. it just makes everything snappier.
#EVENTS_PUSH_BACKEND = "taiga.events.backends.rabbitmq.EventsPushBackend"
#EVENTS_PUSH_BACKEND_OPTIONS = {"url": "amqp://taiga:{{ taiga_events_password }}@localhost:5672/taiga"}
#
#from .celery import *
#
#BROKER_URL = 'amqp://guest:guest@localhost:5672//'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
#CELERY_ENABLED = True

# Uncomment and populate with proper connection parameters
# for enable email sending.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = False
EMAIL_HOST = "localhost"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 25
