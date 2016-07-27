# Configuration file for pps aka the plus-plus-service

SQLALCHEMY_DATABASE_URI = 'postgresql://{{ pps_db_user }}:{{ pps_db_pass }}@{{ pps_db_host }}/{{ pps_db_name }}'

## name of the user so the application can log in to FAS with
FAS_USERNAME = '{{ fedorathirdpartyUser }}'
## password of the user so the application can log in to FAS with
FAS_PASSWORD = '{{ fedorathirdpartyPassword }}'

PLUS_PLUS_TOKEN = '{{ plus_plus_service_token }}'

{% if env == 'staging' %}
FAS_URL = 'https://admin.stg.fedoraproject.org/accounts/'
{% else %}
FAS_URL = 'https://admin.fedoraproject.org/accounts/'
{% endif %}
