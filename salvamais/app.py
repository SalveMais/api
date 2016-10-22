# encoding:utf-8
import os

from flask import Flask
from conf import conf


def create_app(env=None):

    if not env:
        env = os.environ.get('SALVAMAIS_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(conf[env])

    return app
