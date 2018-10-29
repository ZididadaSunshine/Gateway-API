import datetime

import jwt
from flask import request

from app.main import db
from app.main.config import secret
from app.main.model.account_model import Account
from app.main.model.invalid_token_model import InvalidToken


class AuthorizationResponse:
    Success = 200
    InvalidCredentials = 400
    Unauthorized = 401


def get_account_id():
    return get_account_id_from_token(get_token())


def get_token():
    return request.headers.get('Authorization')


def get_account_id_from_token(token):
    if not token:
        return None

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


def logout():
    token = get_token()

    if token:
        invalid_token = InvalidToken(token=token, creation_date=datetime.datetime.utcnow())

        db.session.add(invalid_token)
        db.session.commit()

    return dict(message='Logout successful.'), AuthorizationResponse.Success
