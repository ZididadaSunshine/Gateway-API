import datetime

from app.main import db
from app.main.model.account_model import Account


class AccountServiceResponse:
    Created = 201
    AlreadyExists = 400


def create_account(data):
    existing = Account.query.filter_by(email=data['email']).first()

    if not existing:
        account = Account(email=data['email'], first_name=data['first_name'], last_name=data['last_name'],
                          creation_date=datetime.datetime.utcnow())
        account.set_password(data['password'])

        db.session.add(account)
        db.session.commit()

        return dict(message='Account successfully created.'), AccountServiceResponse.Created
    else:
        return dict(message=f'E-mail address is already in use.'), AccountServiceResponse.AlreadyExists
