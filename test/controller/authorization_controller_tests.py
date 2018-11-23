import json
from unittest import mock

from app.main.service.authorization_service import AuthorizationResponse
from test.base.base_testcase import BaseTestCase


class AuthorizationControllerTests(BaseTestCase):
    def test_login_empty(self):
        """ Test an empty login request """
        response = self.client.post('/api/authorization/login', content_type='application/json')

        self.assert400(response)

    def test_login_partial(self):
        """ Test a partial login request """
        response = self.client.post('/api/authorization/login', content_type='application/json',
                                    data=json.dumps(dict(email='test@example.com')))

        self.assert400(response)

    @mock.patch('app.main.service.authorization_service.login')
    def test_login_invalid(self, mock_login):
        """ Test a login request with an invalid wrong credentials response """
        mock_login.return_value = dict(success=False,
                                       message='Invalid credentials.'), AuthorizationResponse.InvalidCredentials

        response = self.client.post('/api/authorization/login', content_type='application/json',
                                    data=json.dumps(self.get_sample_credentials()))

        self.assertEqual(response.status_code, AuthorizationResponse.InvalidCredentials)
        self.assertFalse(response.json['success'])

    @mock.patch('app.main.service.authorization_service.login')
    def test_login_valid(self, mock_login):
        """ Test a login request with a valid response """
        token = 'example token'
        mock_login.return_value = dict(success=True,
                                       token=token), AuthorizationResponse.Success

        response = self.client.post('/api/authorization/login', content_type='application/json',
                                    data=json.dumps(self.get_sample_credentials()))

        self.assertEqual(response.status_code, AuthorizationResponse.Success)
        self.assertEqual(response.json['token'], token)
        self.assertTrue(response.json['success'])

    @mock.patch('app.main.service.authorization_service.logout')
    def test_logout_with_token(self, mock_logout):
        """ Test a logout request with a token """
        mock_logout.return_value = dict(success=True), AuthorizationResponse.Success

        response = self.client.get('/api/authorization/logout', headers={'Authorization': 'Test'})

        self.assertEqual(response.status_code, AuthorizationResponse.Success)
        self.assertTrue(response.json['success'])

    @mock.patch('app.main.service.authorization_service.logout')
    def test_logout_no_token(self, mock_logout):
        """ Test a logout request without a token """
        mock_logout.return_value = dict(success=True), AuthorizationResponse.Success

        response = self.client.get('/api/authorization/logout')

        self.assertEqual(response.status_code, AuthorizationResponse.Success)
        self.assertTrue(response.json['success'])
