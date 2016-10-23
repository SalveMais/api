from flask import request

from . import accounts
from .auth import basic_auth


@accounts.route('/login', methods=['POST'])
def new_user():
    return 'Michael required', 200


@accounts.route('/', methods=['GET'])
@basic_auth.login_required
def required_auth_example():
    pass
