import datetime

from app.main import db
from app.main.model.account_model import Account
from app.main.service.authorization_service import login, AuthorizationResponse, encode_token, \
    get_account_id_from_token, is_authorized, logout, is_key_correct
from test.base.database_testcase import DatabaseTestCase


class AuthorizationServiceTests(DatabaseTestCase):
    def _get_account(self):
        sample = self.get_sample_account()
        account = Account(email=sample['email'],
                          username=sample['username'],
                          created_at=datetime.datetime.utcnow())
        account.set_password(sample['password'])

        return account

    @staticmethod
    def _add_account(account):
        db.session.add(account)
        db.session.commit()

    def test_incorrect_key(self):
        """ Test that an incorrect API key is rejected """
        self.assertFalse(is_key_correct('not' + self.app.config['API_KEY']))

    def test_correct_key(self):
        """ Test that a correct API key is accepted """
        self.assertTrue(is_key_correct(self.app.config['API_KEY']))

    def test_correct_password(self):
        """ Test that a correct password is accepted."""
        account = self._get_account()

        self.assertTrue(account.check_password(self.get_sample_account()['password']))

    def test_incorrect_password(self):
        """ Test that an incorrect password is rejected."""
        account = self._get_account()

        self.assertFalse(account.check_password('not' + self.get_sample_account()['password']))

    def test_existing_account_valid(self):
        """ Test that an existing account can login with correct details """
        self._add_account(self._get_account())

        login_dict, login_code = login(self.get_sample_credentials())

        self.assertTrue(login_dict['success'])
        self.assertEqual(login_code, AuthorizationResponse.Success)
        self.assertIn('token', login_dict)

    def test_existing_account_invalid(self):
        """ Test that an existing account cannot login with wrong credentials."""
        self._add_account(self._get_account())

        invalid_credentials = self.get_sample_credentials()
        invalid_credentials['password'] += 'invalid'

        login_dict, login_code = login(invalid_credentials)

        self.assertFalse(login_dict['success'])
        self.assertEqual(login_code, AuthorizationResponse.InvalidCredentials)

    def test_unexisting_account(self):
        """ Test that a login fails with an unexisting account."""
        login_dict, login_code = login(self.get_sample_credentials())

        self.assertFalse(login_dict['success'])
        self.assertEqual(login_code, AuthorizationResponse.InvalidCredentials)

    def test_id_from_token(self):
        """ Test that an identifier can be extracted from a token """
        account = self._get_account()
        account.id = 1

        token = encode_token(account)

        self.assertEqual(get_account_id_from_token(token), account.id)

    def test_authorized(self):
        """ Test that a session with a valid token is authorized """
        self._add_account(self._get_account())

        token = login(self.get_sample_credentials())[0]['token']

        self.assertTrue(is_authorized(token))

    def test_logout_authorized(self):
        """ Test that the token is unauthorized after logging out """
        self._add_account(self._get_account())

        token = login(self.get_sample_credentials())[0]['token']
        logout(token)

        self.assertFalse(is_authorized(token))

    def test_logout_invalid_token(self):
        """ Test that logging out is possible without a token """
        logout_dict, logout_code = logout()

        self.assertTrue(logout_dict['success'])
        self.assertEqual(logout_code, AuthorizationResponse.Success)

    def test_logout_valid_token(self):
        """ Test that logout works with valid tokens"""
        self._add_account(self._get_account())

        token = login(self.get_sample_credentials())[0]['token']
        logout_dict, logout_code = logout(token)

        self.assertTrue(logout_dict['success'])
        self.assertEqual(logout_code, AuthorizationResponse.Success)
