from flask import jsonify, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from ..models import User


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')


@basic_auth.verify_password
def verify_password(email, password):
    """This is the email/password verification callback."""
    user = User.objects.filter(email=email).first()
    if user is None or not user.verify_password(password):
        return False
    g.current_user = user
    return True


@basic_auth.error_handler
def password_invalid():
    """Return 401 to the client when password is invalid."""
    error_message = jsonify({'error': 'invalid email or password'})
    return (error_message, 401,
            {'WWW-Authenticate': 'Bearer realm="Invalid email or password"'})


@token_auth.verify_token
def verify_auth_token(token):
    """This is the token verification callback."""
    user = User.objects.filter(auth_token=token).first()
    if user is None:
        return False
    g.current_user = user
    return True


@token_auth.error_handler
def token_invalid():
    """Returns 401 to the client when token is invalid."""
    error_message = jsonify({'error': 'Authorization required'})
    return (error_message, 401,
            {'WWW-Authenticate': 'Bearer realm="Authentication required"'})
