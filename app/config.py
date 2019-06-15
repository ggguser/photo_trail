import os


class Config(object):
    IMAGE_DIR = os.path.join('static', 'photos')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this_is_secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///phototrail.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
