import datetime

from app.main.model.account_model import Account
from app.main.model.brand_model import Brand
from test.base.base_testcase import BaseTestCase
from app.main import db


# The test base is used for all tests that require database connectivity
# This ensure that tables are created when tests are setup and dropped when a test is done
class DatabaseTestCase(BaseTestCase):
    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @staticmethod
    def _create_dummy_brand(account_id, name):
        brand = Brand(account_id=account_id, name=name, creation_date=datetime.datetime.utcnow())

        db.session.add(brand)
        db.session.commit()

        db.session.refresh(brand)

        return brand

    @staticmethod
    def _create_dummy_account(email):
        account = Account(email=email, first_name='Dummy', last_name='Dummy',
                          creation_date=datetime.datetime.utcnow())
        account.set_password('dummy')

        db.session.add(account)
        db.session.commit()

        db.session.refresh(account)

        return account
