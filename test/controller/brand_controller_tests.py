import datetime
import json
import unittest
from unittest import mock

from app.main.model.brand_model import Brand
from app.main.model.synonym_model import Synonym
from app.main.service.authorization_service import AuthorizationResponse
from app.main.service.brand_service import BrandServiceResponse
from test.base.base_testcase import BaseTestCase


def get_sample_instance(brand_id):
    return Brand(name=BaseTestCase.get_sample_brand()['name'], id=brand_id)


def get_sample_instances():
    return [get_sample_instance(1), get_sample_instance(2)]


def get_new_name_sample():
    return {'name': 'Test'}


def get_sample_synonym(name):
    return Synonym(synonym=name)


def get_sample_synonyms():
    return [get_sample_synonym('aau'), get_sample_synonym('aalborg university')]


class BrandControllerTests(BaseTestCase):
    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=False)
    def test_create_brand_unauthorized(self, _mock_authorized):
        """ Test an unauthorized brand creation attempt """
        response = self.client.post('/brands', content_type='application/json',
                                    data=json.dumps(self.get_sample_brand()))

        self.assertEqual(response.status_code, AuthorizationResponse.Unauthorized)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.create_brand', return_value=(dict(success=True), BrandServiceResponse.Created))
    def test_create_brand_authorized(self, _mock_authorized, _mock_create):
        """ Test an authorized brand creation attempt with proper data """
        response = self.client.post('/brands', content_type='application/json',
                                    data=json.dumps(self.get_sample_brand()))

        self.assertEqual(response.status_code, BrandServiceResponse.Created)
        self.assertTrue(response.json['success'])

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    def test_create_brand_authorized_empty(self, _mock_authorized):
        """ Test an authorized brand creation attempt with no data """
        response = self.client.post('/brands', content_type='application/json')

        self.assert400(response)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=False)
    def test_get_brands_unauthorized(self, _mock_authorized):
        """ Test an unauthorized brand creation attempt """
        response = self.client.get('/brands')

        self.assertEqual(response.status_code, AuthorizationResponse.Unauthorized)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brands_by_account', return_value=get_sample_instances())
    def test_get_brands_authorized(self, _mock_authorized, _mock_get_brands):
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
    def test_delete_brand_unauthorized(self, _mock_authorized):
        """ Test an unauthorized brand deletion attempt """
        response = self.client.delete('/brands/1')

        self.assertEqual(response.status_code, AuthorizationResponse.Unauthorized)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brand_by_id', return_value=None)
    def test_delete_brand_authorized_unexisting(self, _mock_authorized, _mock_get):
        """ Test an authorized brand deletion attempt on an unexisting brand """
        response = self.client.delete('/brands/1')

        self.assertEqual(response.status_code, BrandServiceResponse.DoesNotExist)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brand_by_id', return_value=get_sample_instance(1))
    @mock.patch('app.main.service.brand_service.delete_brand',
                return_value=(dict(success=True), BrandServiceResponse.Success))
    def test_delete_brand_authorized_existing(self, _mock_authorized, _mock_get, _mock_delete):
        """ Test an authorized brand deletion attempt on an existing brand """
        response = self.client.delete('/brands/1')

        self.assertEqual(response.status_code, BrandServiceResponse.Success)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=False)
    def test_get_brand_unauthorized(self, _mock_authorized):
        """ Test an unauthorized brand retrieval  """
        response = self.client.get('/brands/1')

        self.assertEqual(response.status_code, AuthorizationResponse.Unauthorized)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brand_by_id', return_value=None)
    def test_get_brand_authorized_unexisting(self, _mock_authorized, _mock_get):
        """ Test an authorized brand retrieval of an unexisting brand  """
        response = self.client.get('/brands/1')

        self.assertEqual(response.status_code, BrandServiceResponse.DoesNotExist)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brand_by_id', return_value=get_sample_instance(1))
    def test_get_brand_authorized_existing(self, _mock_authorized, _mock_get):
        """ Test an authorized brand retrieval of an existing brand """
        response = self.client.get('/brands/1')

        instance = get_sample_instance(1)
        self.assertEqual(response.json['id'], instance.id)
        self.assertEqual(response.json['name'], instance.name)
        self.assertEqual(response.status_code, BrandServiceResponse.Success)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=False)
    def test_update_brand_unauthorized(self, _mock_authorized):
        """ Test an unauthorized brand update  """
        response = self.client.put('/brands/1', content_type='application/json',
                                   data=json.dumps(get_new_name_sample()))

        self.assertEqual(response.status_code, AuthorizationResponse.Unauthorized)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    def test_update_brand_authorized_partial(self, _mock_authorized):
        """ Test an authorized partial brand update  """
        response = self.client.put('/brands/1', content_type='application/json')

        self.assert400(response)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brand_by_id', return_value=None)
    def test_update_brand_authorized_unexisting(self, _mock_authorized, _mock_get):
        """ Test an authorized brand update on an unexisting brand  """
        response = self.client.put('/brands/1', content_type='application/json',
                                   data=json.dumps(get_new_name_sample()))

        self.assertEqual(response.status_code, BrandServiceResponse.DoesNotExist)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brand_by_id', return_value=get_sample_instance(1))
    @mock.patch('app.main.service.brand_service.update_brand',
                return_value=(dict(success=True), BrandServiceResponse.Success))
    def test_update_brand_authorized_existing(self, _mock_authorized, _mock_get, _mock_update):
        """ Test an authorized brand update on an existing brand  """
        response = self.client.put('/brands/1', content_type='application/json',
                                   data=json.dumps(get_new_name_sample()))

        self.assertEqual(response.status_code, BrandServiceResponse.Success)
        self.assertTrue(response.json['success'])

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=False)
    def test_get_synonyms_unauthorized(self, _mock_authorized):
        """ Test an unauthorized synonym retrieval for a brand"""
        response = self.client.get('/brands/1/synonyms')

        self.assertEqual(response.status_code, AuthorizationResponse.Unauthorized)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brand_by_id', return_value=None)
    def test_get_synonyms_authorized_unexisting(self, _mock_authorized, _mock_get):
        """ Test an authorized synonym retrieval for an unexisting brand"""
        response = self.client.get('/brands/1/synonyms')

        self.assertEqual(response.status_code, BrandServiceResponse.DoesNotExist)

    @mock.patch('app.main.service.authorization_service.is_authorized', return_value=True)
    @mock.patch('app.main.service.brand_service.get_brand_by_id', return_value=get_sample_instance(1))
    @mock.patch('app.main.service.synonym_service.get_brand_synonyms', return_value=get_sample_synonyms())
    def test_get_synonyms_authorized_existing(self, _mock_authorized, _mock_get_brand, _mock_get_synoynms):
        """ Test an authorized synonym retrieval for an existing brand"""
        response = self.client.get('/brands/1/synonyms')

        self.assertEqual(response.status_code, BrandServiceResponse.Success)

        # Test that all synonyms are present
        self.assertTrue(set(response.json) == set([synonym.synonym for synonym in get_sample_synonyms()]))


if __name__ == "__main__":
    unittest.main()
