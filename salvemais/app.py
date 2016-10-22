import os

from flask import Flask
from confs import confs


def create_app(env=None):
    """Returns a Flask App instance."""
    if env is None:
        env = os.environ.get('SALVAMAIS_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(confs[env])

    # registering api blueprint
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v1')

    return app
