from flask import current_app, request, url_for, session

from .. import oauth
from . import accounts
from ..models import Donor


token_getter = ''

facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=current_app.config['FACEBOOK_APP_ID'],
    consumer_secret=current_app.config['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'}
)


@facebook.tokengetter
def facebook_tokengetter(token=None):
    print('#' * 100)
    return token_getter


@accounts.route('/login', methods=['GET'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')

    try:
        donor = Donor.objects.get(email=email)
        response = {
            'next': "/dashboard"
        }

    except Donor.DoesNotExist:
        donor = Donor(email=email, password=password)
        response = {
            'next': "/signup"
        }
    token = donor.login(password=password)

    return response.update({
        'token': token,
        'status': True,
    })


@accounts.route('/facebook', methods=['GET'])
def login_facebook():
    next_url = request.args.get('next') or request.referrer or None
    callback = url_for(
        'accounts.facebook_authorized',
        next=next_url,
        _external=True,
    )
    client = facebook.make_client()
    params = dict(facebook.request_token_params) or {}
    session['{}_oauthredir'.format(facebook.name)] = callback
    url = client.prepare_request_uri(
        facebook.expand_url(facebook.authorize_url),
        redirect_uri=callback,
        **params
    )
    return url


@accounts.route('/login/authorized', methods=['GET'])
def facebook_authorized():
    facebook_resp = facebook.authorized_response()
    print(facebook_resp, '#')
    if facebook_resp is None:
        return 'Deu ruim!!!', 403
    return 'Deu bom!!!'
