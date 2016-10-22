import os

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_oauthlib.client import OAuth

from confs import confs


db = MongoEngine()
oauth = OAuth()


def create_app(env=None):
    """Returns a Flask App instance."""
    if env is None:
        env = os.environ.get('SALVEMAIS_CONFIG', 'dev')

    app = Flask(__name__)
    app.config.from_object(confs[env])

    # register plugins
    db.init_app(app)
    oauth.init_app(app)

    with app.app_context() as app_ctx:
        # registering api blueprint
        from .accounts import accounts as accounts_blueprint
        app.register_blueprint(accounts_blueprint, url_prefix='/v1')

    return app
