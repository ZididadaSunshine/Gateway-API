import unittest

from app.main.service.account_service import create_account, AccountServiceResponse
from test.base.database_testcase import DatabaseTestCase


class AccountServiceTests(DatabaseTestCase):
    def _test_create(self, details, expected_success=True, expected_code=AccountServiceResponse.Created):
        response, code = create_account(details)

        self.assertEquals(response['success'], expected_success)
        self.assertEquals(code, expected_code)

    def test_create_single(self):
        """ Test that an account can be created """
        self._test_create(self._get_sample_account())

    def test_create_multiple(self):
        """ Test that multiple accounts can be created with different e-mails """
        self._test_create(self._get_sample_account())

        # Use another e-mail for the other attempt
        aux_details = self._get_sample_account().copy()
        aux_details['email'] = 'another@example.com'

        self._test_create(aux_details)

    def test_duplicate_creation(self):
        """ Test that multiple accounts cannot use the same e-mail """
        # Ignore the result of the first account creation
        create_account(self._get_sample_account())

        self._test_create(self._get_sample_account(), expected_success=False,
                          expected_code=AccountServiceResponse.AlreadyExists)


if __name__ == "__main__":
    unittest.main()
