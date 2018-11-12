from unittest import mock

from app.main.service.authorization_service import AuthorizationResponse
from app.main.service.synonym_service import SynonymServiceResponse
from test.base.base_testcase import BaseTestCase


class SynonymControllerTests(BaseTestCase):
    @mock.patch('app.main.service.authorization_service.is_key_correct', return_value=False)
    def test_get_synonyms_unauthorized(self, _mock_authorize):
        """ Test retrieval of synonyms without authorization """
        response = self.client.get('/synonyms')

        self.assertEqual(response.status_code, AuthorizationResponse.Unauthorized)

    @mock.patch('app.main.service.authorization_service.is_key_correct', return_value=True)
    @mock.patch('app.main.service.synonym_service.get_active_synonyms',
                return_value=[('aau', 1)])
    def test_get_synonyms_authorized(self, _mock_authorize, _mock_get_synonyms):
        """ Test retrieval of synonyms with authorization """
        response = self.client.get('/synonyms')

        self.assertEqual(response.status_code, SynonymServiceResponse.Success)
        self.assertIn('aau', response.json)
        self.assertEqual(response.json['aau'], 1)
