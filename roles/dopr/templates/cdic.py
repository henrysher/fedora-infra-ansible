
# coding: utf-8

DOCKERHUB_URL = 'https://hub.docker.com'
DOCKERREGISTRY_URL = 'https://registry.hub.docker.com'
DOCKERHUB_USERNAME = '{{ dopr_testing_dockerhub_username }}'
DOCKERHUB_PASSWORD = '{{ dopr_testing_dockerhub_password }}'
HUB_PROJECT_URL_TEMPLATE = 'http://registry.hub.docker.com/u/cdictest/{repo_name}'

GITHUB_TOKEN = '{{ dopr_testing_github_token }}'
GITHUB_USER = '{{ dopr_testing_github_username }}'
GITHUB_PASSWORD = '{{ dopr_testing_github_password }}'
GITHUB_API_ROOT = 'https://api.github.com'

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://cdic:{{ dopr_db_passwd }}@localhost/cdicdb'
DATABASE_CONNECT_OPTIONS = {}

VAR_ROOT = '/var/lib/cdic'
OPENID_STORE = '/var/lib/cdic/openid'
CDIC_WORKPLACE = '/var/lib/cdic/wp'
