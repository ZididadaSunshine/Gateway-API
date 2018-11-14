import datetime

from app.main.model.account_model import Account
from app.main.model.brand_model import Brand
from app.main.model.brand_synonym_association import BrandSynonym
from app.main.model.synonym_model import Synonym
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
    def _create_dummy_synonym(synonym):
        synonym = Synonym(synonym=synonym)

        db.session.add(synonym)
        db.session.commit()
        db.session.refresh(synonym)

        return synonym

    @staticmethod
    def _create_dummy_association(brand_id, synonym_id):
        association = BrandSynonym(brand_id=brand_id, synonym_id=synonym_id, created_at=datetime.datetime.utcnow())

        db.session.add(association)
        db.session.commit()
        db.session.refresh(association)

        return association

    @staticmethod
    def _create_dummy_brand(account_id, name):
        brand = Brand(account_id=account_id, name=name, created_at=datetime.datetime.utcnow())

        db.session.add(brand)
        db.session.commit()
        db.session.refresh(brand)

        return brand

    @staticmethod
    def _create_dummy_account(email):
        account = Account(email=email, first_name='Dummy', last_name='Dummy',
                          created_at=datetime.datetime.utcnow())
        account.set_password('dummy')

        db.session.add(account)
        db.session.commit()
        db.session.refresh(account)

        return account
