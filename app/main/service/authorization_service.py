import datetime
from functools import wraps

import jwt
from flask import request

from app.main.config import secret
from app.main.model.account_model import Account


class AuthorizationResponse:
    Success = 200
    InvalidCredentials = 400
    Unauthorized = 401


def require_authorization(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if token:
            decoded_token = decode_token(token)

            if decoded_token:
                return f(*args, **kwargs)

        # Either no token was provided or it is invalid
        # Either way, return an unauthorized response
        return dict(message='You are not authorized to perform this request.'), AuthorizationResponse.Unauthorized

    return decorated


def decode_token(token):
    try:
        return jwt.decode(token, secret)['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def encode_token(account):
    payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1), 'iat': datetime.datetime.utcnow(),
               'sub': account.id}

    # The decode call at the end simply decodes the JWT to a string, it does not actually decode the token
    return jwt.encode(payload, secret, algorithm='HS256').decode()


def login(data):
    account = Account.query.filter_by(email=data['email']).first()
    if account and account.check_password(data['password']):
        return dict(message='Successful login.', token=encode_token(account)), AuthorizationResponse.Success
    else:
        return dict(message='Invalid credentials.'), AuthorizationResponse.InvalidCredentials
