from .common import *

MEDIA_URL = "https://{{ inventory_hostname }}/media/"
STATIC_URL = "https://{{ inventory_hostname }}/static/"
ADMIN_MEDIA_PREFIX = "https://{{ inventory_hostname }}/static/admin/"
SITES["front"]["scheme"] = "https"
SITES["front"]["domain"] = "{{ inventory_hostname }}"

SECRET_KEY = "{{ taiga_secret_key }}"

DEBUG = False
TEMPLATE_DEBUG = False
PUBLIC_REGISTER_ENABLED = True

DEFAULT_FROM_EMAIL = "nobody@fedoraproject.org"
SERVER_EMAIL = DEFAULT_FROM_EMAIL

INSTALLED_APPS += [
    "mozilla_django_oidc",
    "taiga_contrib_oidc_auth",
]

AUTHENTICATION_BACKENDS = list(AUTHENTICATION_BACKENDS) + [
    "taiga_contrib_oidc_auth.oidc.TaigaOIDCAuthenticationBackend",
]

# OIDC Settings
OIDC_CALLBACK_CLASS = "taiga_contrib_oidc_auth.views.TaigaOIDCAuthenticationCallbackView"
OIDC_RP_SCOPES = "openid profile email"
OIDC_RP_SIGN_ALGO = "RS256"
# Set the OIDC provider here.
OIDC_BASE_URL = "https://id{{ env_suffix }}.fedoraproject.org/openidc"
# Those URL values work for Ipsilon.
OIDC_OP_JWKS_ENDPOINT = OIDC_BASE_URL + "/Jwks"
OIDC_OP_AUTHORIZATION_ENDPOINT = OIDC_BASE_URL + "/Authorization"
OIDC_OP_TOKEN_ENDPOINT = OIDC_BASE_URL + "/Token"
OIDC_OP_USER_ENDPOINT = OIDC_BASE_URL + "/UserInfo"
# These two are private! Don't commit them to VCS.
OIDC_RP_CLIENT_ID = "{{ taiga_stg_oidc_client_id }}"
OIDC_RP_CLIENT_SECRET = "{{ taiga_stg_oidc_client_secret }}"

# Add the OIDC urls
ROOT_URLCONF = "settings.urls"

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
