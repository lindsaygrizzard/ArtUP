import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '\x12`(\x1dF&\xe964_v\xf5\xa2\x91\x9da\xc1#\x1dh\x96\xfe\xe8\xb4'
    SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
