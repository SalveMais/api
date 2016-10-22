import os

from flask import Flask
from flask_mongoengine import MongoEngine

from confs import confs


db = MongoEngine()


def create_app(env=None):
    """Returns a Flask App instance."""
    if env is None:
        env = os.environ.get('SALVEMAIS_CONFIG', 'dev')

    app = Flask(__name__)
    app.config.from_object(confs[env])

    # register plugins
    db.init_app(app)

    # registering api blueprint
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v1')

    return app
