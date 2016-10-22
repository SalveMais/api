# encoding:utf-8
import os


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    GENDERS = (
        ('M', 'Masculino'),
        ('F', 'Feminino')
    )

    BLOOD_RATIO = {
        'M': 62.4,
        'F': 61.9
    }


class TestConfig(Config):
    TESTING = True
    DATABASE_NAME = 'salvemais_test'
    MONGODB_SETTINGS = {'DB': DATABASE_NAME}


class DevConfig(Config):
    DATABASE_NAME = 'salvemais_dev'
    MONGODB_SETTINGS = {'DB': DATABASE_NAME}

    SOCIAL_FACEBOOK = {
        'consumer_key': '1825953660954282',
        'consumer_secret': '5238121e7b618c1f3ec1df41872f6711'
    }


class ProdConfig(Config):
    DATABASE_NAME = 'salvemais'
    MONGODB_SETTINGS = {'DB': DATABASE_NAME}


confs = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig,
}
