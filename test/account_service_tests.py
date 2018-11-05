import unittest

from app.main.service.account_service import create_account, AccountServiceResponse
from test.base_testcase import BaseTestCase
from test.database_testcase import DatabaseTestCase


class AccountServiceTests(DatabaseTestCase):
    def _test_create(self, details, expected_success=True, expected_code=AccountServiceResponse.Created):
        response, code = create_account(details)

        self.assertEquals(response['success'], expected_success)
        self.assertEquals(code, expected_code)

    def test_create_single(self):
        self._test_create(BaseTestCase.AccountSample)

    def test_create_multiple(self):
        self._test_create(BaseTestCase.AccountSample)

        # Use another e-mail for the other attempt
        aux_details = BaseTestCase.AccountSample.copy()
        aux_details['email'] = 'another@example.com'

        self._test_create(aux_details)

    def test_duplicate_creation(self):
        # Ignore the result of the first account creation
        create_account(BaseTestCase.AccountSample)

        self._test_create(BaseTestCase.AccountSample, expected_success=False,
                          expected_code=AccountServiceResponse.AlreadyExists)


if __name__ == "__main__":
    unittest.main()
