import json
import unittest
from unittest import mock

from app.main.service.account_service import AccountServiceResponse
from test.base.base_testcase import BaseTestCase


class AccountControllerTests(BaseTestCase):
    def test_create_empty(self):
        """ Test an empty account creation """
        response = self.client.post('/accounts', content_type='application/json')

        self.assert400(response)

    def test_create_partial(self):
        """ Test a partial account creation"""
        sample = self._get_sample_account()
        del sample['password']

        response = self.client.post('/accounts', data=json.dumps(sample), content_type='application/json')

        self.assert400(response)

    @mock.patch('app.main.service.account_service.create_account')
    def test_create_succeeds(self, mock_create):
        """ Test a successful account creation """
        # Mock a successful creation
        mock_create.return_value = dict(success=True), AccountServiceResponse.Created

        response = self.client.post('/accounts', data=json.dumps(self._get_sample_account()),
                                    content_type='application/json')

        self.assertTrue(response.json['success'])
        self.assertEqual(response.status_code, AccountServiceResponse.Created)

    @mock.patch('app.main.service.account_service.create_account')
    def test_create_fails(self, mock_create):
        """ Test an unsuccessful account creation """
        # Mock a failed creation
        mock_create.return_value = dict(success=False), AccountServiceResponse.AlreadyExists

        response = self.client.post('/accounts', data=json.dumps(self._get_sample_account()),
                                    content_type='application/json')

        self.assertFalse(response.json['success'])
        self.assertEqual(response.status_code, AccountServiceResponse.AlreadyExists)


if __name__ == "__main__":
    unittest.main()
