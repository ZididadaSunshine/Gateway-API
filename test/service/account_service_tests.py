import unittest

from app.main.model.account_model import Account
from app.main.service.account_service import create_account, AccountServiceResponse
from test.base.database_testcase import DatabaseTestCase


class AccountServiceTests(DatabaseTestCase):
    def _test_create(self, details, expected_success=True, expected_code=AccountServiceResponse.Created,
                     test_account_existence=True):
        response, code = create_account(details)

        self.assertEqual(response['success'], expected_success)
        self.assertEqual(code, expected_code)

        if test_account_existence:
            account = Account.query.filter_by(email=details['email']).first()

            self.assertIsNotNone(account)
            self.assertEqual(account.email, details['email'])
            self.assertEqual(account.username, details['username'])
            self.assertTrue(account.check_password(details['password']))

    def test_create_single(self):
        """ Test that an account can be created """
        self._test_create(self.get_sample_account())

    def test_create_multiple(self):
        """ Test that multiple accounts can be created with different e-mails """
        self._test_create(self.get_sample_account())

        # Use another e-mail for the other attempt
        aux_details = self.get_sample_account()
        aux_details['email'] = 'another@example.com'

        self._test_create(aux_details)

    def test_duplicate_creation(self):
        """ Test that multiple accounts cannot use the same e-mail """
        # Ignore the result of the first account creation
        create_account(self.get_sample_account())

        self._test_create(self.get_sample_account(), expected_success=False,
                          expected_code=AccountServiceResponse.AlreadyExists, test_account_existence=False)


if __name__ == "__main__":
    unittest.main()
