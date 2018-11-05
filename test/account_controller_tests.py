import unittest

import json

from test.base_testcase import BaseTestCase


class AccountControllerTests(BaseTestCase):
    def test_create_empty(self):
        response = self.client.post('/accounts', content_type='application/json')

        self.assert400(response)

    def test_create_partial(self):
        sample = BaseTestCase.AccountSample.copy()
        del sample['password']

        response = self.client.post('/accounts', data=json.dumps(sample), content_type='application/json')

        self.assert400(response)

    def test_create_succeeds(self):
        response = self.client.post('/accounts', data=json.dumps(BaseTestCase.AccountSample),
                                    content_type='application/json')
        print(response)

        self.assert200(response)


if __name__ == "__main__":
    unittest.main()
