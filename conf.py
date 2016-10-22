# encoding:utf-8

class Config:
	DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_NAME = 'twegeo'
    MONGODB_SETTINGS = {'DB': DATABASE_NAME}


class DevelpmentConfig(Config):
	pass


conf = {
	'development': DevelpmentConfig,
}
