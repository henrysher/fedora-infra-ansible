import config
import constants

SQLALCHEMY_DATABASE_URI = 'postgres://{{modernpaste_stg_db_user}}:{{modernpaste_stg_db_password}}@db01/modernpaste'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask session secret key
SECRET_KEY = config.FLASK_SECRET_KEY
