import datetime
import json
import unittest
from unittest import mock

from app.main.model.brand_model import Brand
from app.main.service.authorization_service import AuthorizationResponse
from app.main.service.brand_service import BrandServiceResponse
from test.base.base_testcase import BaseTestCase


def get_sample_instance(brand_id):
    return Brand(name=BaseTestCase.get_sample_brand()['name'], id=brand_id)


def get_sample_instances():
    return [get_sample_instance(1), get_sample_instance(2)]


class BrandControllerTests(BaseTestCase):
    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=False)
    def test_create_brand_unauthorized(self, mock_authorized):
        """ Test an unauthorized brand creation attempt """
        response = self.client.post('/brands', content_type='application/json',
                                    data=json.dumps(self.get_sample_brand()))

        self.assertEqual(response.status_code, AuthorizationResponse.Unauthorized)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.create_brand', return_value=(dict(success=True), BrandServiceResponse.Created))
    def test_create_brand_authorized(self, mock_authorized, mock_create):
        """ Test an authorized brand creation attempt with proper data """
        response = self.client.post('/brands', content_type='application/json',
                                    data=json.dumps(self.get_sample_brand()))

        self.assertEqual(response.status_code, BrandServiceResponse.Created)
        self.assertTrue(response.json['success'])

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    def test_create_brand_authorized_empty(self, mock_authorized):
        """ Test an authorized brand creation attempt with no data """
        response = self.client.post('/brands', content_type='application/json')

        self.assert400(response)
p
    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=False)
    def test_get_brands_unauthorized(self, mock_authorized):
        """ Test an unauthorized brand creation attempt """
        response = self.client.get('/brands')

        self.assertEqual(response.status_code, AuthorizationResponse.Unauthorized)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brands_by_account', return_value=get_sample_instances())
    def test_get_brands_authorized(self, mock_authorized, mock_get_brands):
        """ Test an authorized brand retrieval attempt """
        response = self.client.get('/brands')

        self.assertEqual(response.status_code, BrandServiceResponse.Success)

        # Assert that all brands are returned
        samples = get_sample_instances()
        for item in response.json:
            instance = next(x for x in samples if item['id'] == x.id)

            self.assertIsNotNone(instance)
            self.assertEqual(instance.id, item['id'])
            self.assertEqual(instance.name, item['name'])

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=False)
    def test_delete_brand_unauthorized(self, mock_authorized):
        """ Test an unauthorized brand deletion attempt """
        response = self.client.delete('/brands/1')

        self.assertEqual(response.status_code, AuthorizationResponse.Unauthorized)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brand_by_id', return_value=None)
    def test_delete_brand_authorized_unexisting(self, mock_authorized, mock_get):
        """ Test an authorized brand deletion attempt on an unexisting brand """
        response = self.client.delete('/brands/1')

        self.assertEqual(response.status_code, BrandServiceResponse.DoesNotExist)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brand_by_id', return_value=get_sample_instance(1))
    @mock.patch('app.main.service.brand_service.delete_brand',
                return_value=(dict(success=True), BrandServiceResponse.Success))
    def test_delete_brand_authorized_existing(self, mock_authorized, mock_get, mock_delete):
        """ Test an authorized brand deletion attempt on an existing brand """
        response = self.client.delete('/brands/1')

        self.assertEqual(response.status_code, BrandServiceResponse.Success)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=False)
    def test_get_brand_unauthorized(self, mock_authorized):
        """ Test an unauthorized brand retrieval  """
        response = self.client.get('/brands/1')

        self.assertEqual(response.status_code, AuthorizationResponse.Unauthorized)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brand_by_id', return_value=None)
    def test_get_brand_authorized_unexisting(self, mock_authorized, mock_get):
        """ Test an authorized brand retrieval of an unexisting brand  """
        response = self.client.get('/brands/1')

        self.assertEqual(response.status_code, BrandServiceResponse.DoesNotExist)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brand_by_id', return_value=get_sample_instance(1))
    def test_get_brand_authorized_existing(self, mock_authorized, mock_get):
        """ Test an authorized brand retrieval of an existing brand """
        response = self.client.get('/brands/1')

        instance = get_sample_instance(1)
        self.assertEqual(response.json['id'], instance.id)
        self.assertEqual(response.json['name'], instance.name)
        self.assertEqual(response.status_code, BrandServiceResponse.Success)


if __name__ == "__main__":
    unittest.main()
