import datetime

from app.main import db
from app.main.model.account_model import Account
from app.main.utility.datalogger import log_time


class AccountServiceResponse:
    Created = 201
    AlreadyExists = 409


@log_time('create_account')
def create_account(user_data):
    existing = Account.query.filter(Account.email.ilike(user_data['email'])).first()

    if not existing:
        account = Account(email=user_data['email'], username=user_data['username'],
                          created_at=datetime.datetime.utcnow())
        account.set_password(user_data['password'])

        db.session.add(account)
        db.session.commit()

        return dict(success=True), AccountServiceResponse.Created
    else:
        return dict(success=False, message=f'E-mail address is already in use.'), AccountServiceResponse.AlreadyExists
