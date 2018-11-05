from test.base_testcase import BaseTestCase
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
