import config
import constants
import os

SQLALCHEMY_DATABASE_URI = "postgres://{{modernpaste_stg_db_user}}:{{modernpaste_stg_db_password}}@db01.stg.phx2.fedoraproject.org/modernpaste"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = config.FLASK_SECRET_KEY
