import os

# default configuration
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = "Shhh! Don't Tell!"
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
