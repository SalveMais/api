from flask import current_app

from . import accounts
from ..models import Donor


@accounts.route('/test', methods=['GET'])
def test_endpoint():
    print(current_app.config, '#')
    return 'Test!!!', 200
