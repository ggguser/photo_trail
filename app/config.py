import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    IMAGE_DIR = os.path.join('app', 'static', 'photos')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this_is_secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///phototrail.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
