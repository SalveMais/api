# encoding:utf-8
import os


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestConfig(Config):
    TESTING = True
    DATABASE_NAME = 'salvamais_test'
    MONGODB_SETTINGS = {'DB': DATABASE_NAME}


class DevConfig(Config):
    DATABASE_NAME = 'salvamais_dev'
    MONGODB_SETTINGS = {'DB': DATABASE_NAME}


class ProdConfig(Config):
    DATABASE_NAME = 'salvamais'
    MONGODB_SETTINGS = {'DB': DATABASE_NAME}


confs = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig,
}
