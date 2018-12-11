import unittest

from app.main import db
from app.main.model.brand_model import Brand
from app.main.model.synonym_model import Synonym
from app.main.service.brand_service import create_brand, BrandServiceResponse, update_brand_name, get_brand_by_id, \
    get_brand_by_name, get_brands_by_account, delete_brand
from test.base.database_testcase import DatabaseTestCase


class BrandServiceTests(DatabaseTestCase):
    def _test_create_brand(self, account_id, details, expected_success=True, expected_code=BrandServiceResponse.Created,
                           expected_message=None, test_brand_existence=True):
        response, code = create_brand(account_id, details)

        self.assertEqual(response['success'], expected_success)
        self.assertEqual(code, expected_code)
        if expected_message:
            self.assertEqual(response['message'], expected_message)
        else:
            self.assertNotIn('message', response)

        if test_brand_existence:
            brand = Brand.query.filter((Brand.name == details['name']) & (Brand.account_id == account_id)).first()

            self.assertIsNotNone(brand)
            self.assertEqual(brand.name, details['name'])
            self.assertEqual(brand.account_id, account_id)

    def test_create_brand_has_synonym(self):
        """ Test that a newly created brand has a default synonym """
        account = self._create_dummy_account('dummy@example.com')
        create_brand(account.id, self.get_sample_brand())

        self.assertTrue(Synonym.query.filter_by(synonym=self.get_sample_brand()['name'].lower()).scalar())

    def test_create_brand_single(self):
        """ Test that a single brand can be created with no duplicates """
        account = self._create_dummy_account('dummy@example.com')

        self._test_create_brand(account.id, self.get_sample_brand())

    def test_create_brand_multiple_different_name(self):
        """ Test that an account can have multiple brands with different names """
        account = self._create_dummy_account('dummy@example.com')

        self._test_create_brand(account.id, self.get_sample_brand())

        aux_details = self.get_sample_brand()
        aux_details['name'] += 'Not'

        self._test_create_brand(account.id, aux_details)

    def test_create_brand_multiple_same_account(self):
        """ Test that the same brand name cannot be created multiple times with the same account """
        account = self._create_dummy_account('dummy@example.com')
        create_brand(account.id, self.get_sample_brand())

        self._test_create_brand(account.id, self.get_sample_brand(), expected_success=False,
                                expected_code=BrandServiceResponse.AlreadyExists, test_brand_existence=False,
                                expected_message='Your account already has a brand with that name.')

    def test_create_brand_multiple_different_accounts(self):
        """ Test that the same brand name can be created multiple times by different accounts """
        first_account = self._create_dummy_account('first@example.com')
        second_account = self._create_dummy_account('second@example.com')

        # Run assertions for the two account ids
        self._test_create_brand(first_account.id, self.get_sample_brand())
        self._test_create_brand(second_account.id, self.get_sample_brand())

    def test_update_brand_no_duplicates(self):
        """ Test that updating the name of a brand results in a new name """
        account = self._create_dummy_account('dummy@example.com')
        brand = self._create_dummy_brand(account.id, 'Initial')

        new_name = 'New'
        response, code = update_brand_name(account.id, brand, {'name': new_name})

        # Assert that attempt succeeded
        self.assertTrue(response['success'])
        self.assertEqual(code, BrandServiceResponse.Success)

        # Assert that name was updated correctly
        db.session.refresh(brand)

        self.assertEqual(brand.name, new_name)

    def test_update_brand_duplicates(self):
        """ Test that a brand name cannot be updated to an account's existing brand name """
        first_name, second_name = 'First', 'Second'

        account = self._create_dummy_account('dummy@example.com')
        first_brand = self._create_dummy_brand(account.id, first_name)
        self._create_dummy_brand(account.id, second_name)

        response, code = update_brand_name(account.id, first_brand, {'name': second_name})

        # Assert that the attempt failed
        self.assertFalse(response['success'])
        self.assertEqual(response['message'], 'Your account already has a brand with that name.')
        self.assertEqual(code, BrandServiceResponse.AlreadyExists)

    def test_get_brand_by_id_existing(self):
        """ Test that an existing brand can be retrieved by ID """
        account = self._create_dummy_account('dummy@example.com')
        brand = self._create_dummy_brand(account.id, 'Brand')

        retrieved = get_brand_by_id(account.id, brand.id)

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, brand.id)

    def test_get_brand_by_id_not_existing(self):
        """ Test that retrieving a non-existing brand by ID returns None """
        account = self._create_dummy_account('dummy@example.com')

        retrieved = get_brand_by_id(account.id, 1)

        self.assertIsNone(retrieved)

    def test_get_brand_by_name(self):
        """ Test that an existing brand can be retrieved by name """
        account = self._create_dummy_account('dummy@example.com')
        brand = self._create_dummy_brand(account.id, 'Brand')

        retrieved = get_brand_by_name(account.id, brand.name)

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, brand.name)

    def test_get_brand_by_name_not_existing(self):
        """ Test that retrieving a non-existing brand by name returns None """
        account = self._create_dummy_account('dummy@example.com')

        retrieved = get_brand_by_name(account.id, 'Brand')

        self.assertIsNone(retrieved)

    def test_get_brands_by_account(self):
        """ Test that retrieving brands from an account yields all the brands """
        account = self._create_dummy_account('dummy@example.com')
        first_brand = self._create_dummy_brand(account.id, 'First')
        second_brand = self._create_dummy_brand(account.id, 'Second')

        retrieved = get_brands_by_account(account.id)

        self.assertIn(first_brand, retrieved)
        self.assertIn(second_brand, retrieved)

    def test_get_brands_by_account_no_brands(self):
        """ Test that retrieving brands from an account with no brands yields no brands """
        account = self._create_dummy_account('dummy@example.com')

        retrieved = get_brands_by_account(account.id)

        self.assertFalse(retrieved)

    def test_delete_brand(self):
        """ Test that deleting a brand actually deletes the brand """
        account = self._create_dummy_account('dummy@example.com')
        brand = self._create_dummy_brand(account.id, 'Brand')

        response, code = delete_brand(brand)

        self.assertTrue(response['success'])
        self.assertEqual(code, BrandServiceResponse.Success)
        self.assertEqual(Brand.query.count(), 0)


if __name__ == "__main__":
    unittest.main()
