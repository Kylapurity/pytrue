"""APP configuration."""
from os import getenv, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

ENVIRONMENT = getenv("ENVIRONMENT")
FLASK_APP = getenv("FLASK_APP")
FLASK_DEBUG = getenv("FLASK_DEBUG")
SECRET_KEY = getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_ECHO = False
WTF_CSRF_ENABLED = False
