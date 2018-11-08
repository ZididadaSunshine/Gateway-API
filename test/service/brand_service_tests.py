import unittest

from app.main import db
from app.main.model.brand_model import Brand
from app.main.service.brand_service import create_brand, BrandServiceResponse, update_brand
from test.base.database_testcase import DatabaseTestCase


class BrandServiceTests(DatabaseTestCase):
    def _test_create_brand(self, account_id, details, expected_success=True, expected_code=BrandServiceResponse.Created,
                           test_brand_existence=True):
        response, code = create_brand(account_id, details)

        self.assertEquals(response['success'], expected_success)
        self.assertEquals(code, expected_code)

        if test_brand_existence:
            brand = Brand.query.filter((Brand.name == details['name']) & (Brand.account_id == account_id)).first()

            self.assertIsNotNone(brand)
            self.assertEquals(brand.name, details['name'])
            self.assertEquals(brand.account_id, account_id)

    def test_create_brand_single(self):
        """ Test whether a single brand can be created with no duplicates """
        account = self._create_dummy_account('dummy@example.com')

        self._test_create_brand(account.id, self._get_sample_brand())

    def test_create_brand_multiple_different_name(self):
        """ Test whether an account can have multiple brands with different names """
        account = self._create_dummy_account('dummy@example.com')

        self._test_create_brand(account.id, self._get_sample_brand())

        aux_details = self._get_sample_brand()
        aux_details['name'] += 'Not'

        self._test_create_brand(account.id, aux_details)

    def test_create_brand_multiple_same_account(self):
        """ Test whether the same brand name cannot be created multiple times with the same account """
        account = self._create_dummy_account('dummy@example.com')
        create_brand(account.id, self._get_sample_brand())

        self._test_create_brand(account.id, self._get_sample_brand(), expected_success=False,
                                expected_code=BrandServiceResponse.AlreadyExists, test_brand_existence=False)

    def test_create_brand_multiple_different_accounts(self):
        """ Test whether the same brand name can be created multiple times by different accounts """
        first_account = self._create_dummy_account('first@example.com')
        second_account = self._create_dummy_account('second@example.com')

        # Run assertions for the two account ids
        self._test_create_brand(first_account.id, self._get_sample_brand())
        self._test_create_brand(second_account.id, self._get_sample_brand())

    def test_update_brand_no_duplicates(self):
        """ Test whether updating the name of a brand results in a new name """
        account = self._create_dummy_account('dummy@example.com')
        brand = self._create_dummy_brand(account.id, 'Initial')

        new_name = 'New'
        response, code = update_brand(account.id, brand, {'name': new_name})

        # Assert that attempt succeeded
        self.assertTrue(response['success'])
        self.assertEquals(code, BrandServiceResponse.Success)

        # Assert that name was updated correctly
        db.session.refresh(brand)

        self.assertEquals(brand.name, new_name)

    def test_update_brand_duplicates(self):
        """ Test whether a brand name cannot be updated to an account's existing brand name """
        first_name, second_name = 'First', 'Second'

        account = self._create_dummy_account('dummy@example.com')
        first_brand = self._create_dummy_brand(account.id, first_name)
        self._create_dummy_brand(account.id, second_name)

        response, code = update_brand(account.id, first_brand, {'name': second_name})

        # Assert that the attempt failed
        self.assertFalse(response['success'])
        self.assertEquals(code, BrandServiceResponse.AlreadyExists)

    def test_get_brand_by_id_existing(self):
        """ Test that an existing brand can be retrieved by ID """



if __name__ == "__main__":
    unittest.main()
