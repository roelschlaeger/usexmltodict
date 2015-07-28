import os


# default configuration
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '&\xcf\xb7M\xe3e\x92W+\x83\x11\xd0s\x89!r~H]e\x99P\xb6='
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    print SQLALCHEMY_DATABASE_URI


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
