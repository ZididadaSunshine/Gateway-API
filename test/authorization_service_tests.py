# Test with newly created account
# Test with non-existing account
# Test with wrong password
import datetime

from app.main import db
from app.main.model.account_model import Account
from app.main.service.authorization_service import login, AuthorizationResponse, encode_token, \
    get_account_id_from_token, is_authorized, logout
from test.base.base_testcase import BaseTestCase
from test.base.database_testcase import DatabaseTestCase


class AuthorizationServiceTest(DatabaseTestCase):
    @staticmethod
    def _get_sample_account():
        account = Account(email=BaseTestCase.AccountSample['email'],
                          first_name=BaseTestCase.AccountSample['first_name'],
                          last_name=BaseTestCase.AccountSample['last_name'],
                          creation_date=datetime.datetime.utcnow())
        account.set_password(BaseTestCase.AccountSample['password'])

        return account

    @staticmethod
    def _get_credentials():
        return {'email': BaseTestCase.AccountSample['email'], 'password': BaseTestCase.AccountSample['password']}

    @staticmethod
    def _add_account(account):
        db.session.add(account)
        db.session.commit()

    def test_correct_password(self):
        account = self._get_sample_account()

        self.assertTrue(account.check_password(BaseTestCase.AccountSample['password']))

    def test_incorrect_password(self):
        account = AuthorizationServiceTest._get_sample_account()

        self.assertFalse(account.check_password('not' + BaseTestCase.AccountSample['password']))

    def test_existing_account_valid(self):
        self._add_account(self._get_sample_account())

        login_dict, login_code = login(self._get_credentials())

        self.assertTrue(login_dict['success'])
        self.assertEquals(login_code, AuthorizationResponse.Success)
        self.assertIn('token', login_dict)

    def test_existing_account_invalid(self):
        self._add_account(self._get_sample_account())

        invalid_credentials = self._get_credentials()
        invalid_credentials['password'] += 'invalid'

        login_dict, login_code = login(invalid_credentials)

        self.assertFalse(login_dict['success'])
        self.assertEquals(login_code, AuthorizationResponse.InvalidCredentials)

    def test_unexisting_account(self):
        login_dict, login_code = login(self._get_credentials())

        self.assertFalse(login_dict['success'])
        self.assertEquals(login_code, AuthorizationResponse.InvalidCredentials)

    def test_id_from_token(self):
        account = self._get_sample_account()
        account.id = 1

        token = encode_token(account)

        self.assertEqual(get_account_id_from_token(token), account.id)

    def test_authorized(self):
        self._add_account(self._get_sample_account())

        token = login(self._get_credentials())[0]['token']

        self.assertTrue(is_authorized(token))

    def test_logout_authorized(self):
        """ Test that the token is unauthorized after logging out. """
        self._add_account(self._get_sample_account())

        token = login(self._get_credentials())[0]['token']
        logout(token)

        self.assertFalse(is_authorized(token))

    def test_logout_invalid_token(self):
        """ Even for invalid tokens, logging out is still valid. """
        logout_dict, logout_code = logout()

        self.assertTrue(logout_dict['success'])
        self.assertEqual(logout_code, AuthorizationResponse.Success)

    def test_logout_valid_token(self):
        self._add_account(self._get_sample_account())

        token = login(self._get_credentials())[0]['token']
        logout_dict, logout_code = logout(token)

        self.assertTrue(logout_dict['success'])
        self.assertEqual(logout_code, AuthorizationResponse.Success)
