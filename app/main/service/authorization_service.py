import datetime

import jwt

from app.main import db
from app.main.config import secret
from app.main.model.account_model import Account
from app.main.model.invalid_token_model import InvalidToken


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


def encode_token(account):
    payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1), 'iat': datetime.datetime.utcnow(),
               'sub': account.id}

    # The decode call at the end simply decodes the JWT to a string, it does not actually decode the token
    return jwt.encode(payload, secret, algorithm='HS256').decode()


def login(credentials):
    account = Account.query.filter(Account.email.ilike(credentials['email'])).first()
    if account and account.check_password(credentials['password']):
        return dict(success=True, token=encode_token(account)), AuthorizationResponse.Success
    else:
        return dict(success=False, message='Invalid credentials.'), AuthorizationResponse.InvalidCredentials


def logout(token=None):
    if token:
        invalid_token = InvalidToken(token=token, creation_date=datetime.datetime.utcnow())

        db.session.add(invalid_token)
        db.session.commit()

    return dict(success=True), AuthorizationResponse.Success
