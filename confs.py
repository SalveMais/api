# encoding:utf-8
import os


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    API_URL = 'http://127.0.0.1:5000'

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
    SECRET_KEY = '\x0c\x81zH\xc9\x9fj\x8e+W\xe6/\xf7M\x80\xb8'
    DATABASE_NAME = 'salvemais_dev'
    MONGODB_SETTINGS = {'DB': DATABASE_NAME}

    FACEBOOK_APP_ID = '1825953660954282'
    FACEBOOK_APP_SECRET = '5238121e7b618c1f3ec1df41872f6711'

    GOOGLE = {
        'maps_api_key': 'AIzaSyDgpP6m3uAQAGqMf4obpVp7KwYwh2nE0bI'
    }


class ProdConfig(Config):
    DATABASE_NAME = 'salvemais'
    MONGODB_SETTINGS = {'DB': DATABASE_NAME}


confs = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig,
}
