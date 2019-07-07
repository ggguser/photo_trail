import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
supported_countries = []


class Config(object):
    IMAGE_DIR = os.path.join('app', 'static', 'photos')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this_is_secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'phototrail.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


class Messages:
    pass


class Country:
    def __init__(self, name, number_of_areas):
        self.name = name
        self.number_of_areas = number_of_areas


russia = Country(name='Россия', number_of_areas=85)

supported_countries.append(russia)






