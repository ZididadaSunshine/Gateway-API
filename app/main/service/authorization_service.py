import datetime

import jwt
from flask import current_app

from app.main import db
from app.main.config import secret
from app.main.model.account_model import Account
from app.main.model.invalid_token_model import InvalidToken
from app.main.utility.datalogger import log_time


class AuthorizationResponse:
    Success = 200
    InvalidCredentials = 400
    Unauthorized = 401


def get_account_id(token):
    return get_account_id_from_token(token)


def get_account_id_from_token(token):
    if not token:
        return None

    try:
        return jwt.decode(token, secret)['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def is_authorized(token=None):
    if token:
        # Check that token is valid
        invalid_token = InvalidToken.query.filter_by(token=token).first()
        if not invalid_token:
            account_id = get_account_id_from_token(token)

            if account_id:
                return True

    return False


def is_key_correct(key=None):
    return key == current_app.config['API_KEY']


def _to_timestamp(date):
    epoch = datetime.datetime(1970, 1, 1)
    return int((date - epoch).total_seconds() * 1000)


def get_token(account):
    expires = _to_timestamp(datetime.datetime.utcnow() + datetime.timedelta(days=1))
    payload = {'exp': expires, 'iat': datetime.datetime.utcnow(), 'sub': account.id}

    # The decode call at the end simply decodes the JWT to a string, it does not actually decode the token
    return expires, jwt.encode(payload, secret, algorithm='HS256').decode()


@log_time('login')
def login(credentials):
    account = Account.query.filter(Account.email.ilike(credentials['email'])).first()
    if account and account.check_password(credentials['password']):
        expires, token = get_token(account)
        return dict(success=True, token=token, expires=expires), AuthorizationResponse.Success
    else:
        return dict(success=False, message='Invalid credentials.'), AuthorizationResponse.InvalidCredentials


@log_time('logout')
def logout(token=None):
    if token:
        invalid_token = InvalidToken(token=token, created_at=datetime.datetime.utcnow())

        db.session.add(invalid_token)
        db.session.commit()

    return dict(success=True), AuthorizationResponse.Success
