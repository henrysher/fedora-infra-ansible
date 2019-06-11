{% if env == 'staging' %}
DATABASE_URI = 'postgresql+psycopg2://waiverdb@db01.stg.phx2.fedoraproject.org:5432/waiverdb'
RESULTSDB_API_URL = 'https://taskotron.stg.fedoraproject.org/resultsdb_api/api/v2.0'
CORS_URL = 'https://bodhi.stg.fedoraproject.org'
MESSAGE_BUS_PUBLISH = True
{% else %}
DATABASE_URI = 'postgresql+psycopg2://waiverdb@db01.phx2.fedoraproject.org:5432/waiverdb'
RESULTSDB_API_URL = 'https://taskotron.fedoraproject.org/resultsdb_api/api/v2.0'
CORS_URL = 'https://bodhi.fedoraproject.org'
MESSAGE_BUS_PUBLISH = False
{% endif %}
AUTH_METHOD = 'OIDC'
OIDC_REQUIRED_SCOPE = 'https://waiverdb.fedoraproject.org/oidc/create-waiver'
OIDC_CLIENT_SECRETS = '/etc/secret/client_secrets.json'
SUPERUSERS = ['bodhi@service']
PORT = 8080
