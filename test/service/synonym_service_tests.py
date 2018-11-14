import unittest

from app.main.model.brand_synonym_association import BrandSynonym
from app.main.model.synonym_model import Synonym
from app.main.service.synonym_service import get_active_synonyms, get_brand_synonyms, add_synonym, \
    SynonymServiceResponse, delete_synonym, preprocess_synonym
from test.base.database_testcase import DatabaseTestCase


class SynonymServiceTests(DatabaseTestCase):
    def _create_n_associations(self, count, brand_name):
        """ Creates n accounts, n brands and n associations where all brands share the same synonym """
        synonym = self._create_dummy_synonym(brand_name.lower())

        accounts = [self._create_dummy_account(f'account{n}@example.com') for n in range(count)]
        brands = [self._create_dummy_brand(accounts[n].id, brand_name) for n in range(count)]
        associations = [self._create_dummy_association(brands[n].id, synonym.id) for n in range(count)]

        return accounts, brands, synonym

    def test_add_synonym_single(self):
        """ Test that adding a single synonym to a brand works """
        brand = self._create_dummy_brand(self._create_dummy_account('account@example.com').id, 'Brand')

        response, code = add_synonym(brand.id, {'synonym': 'Brand'})

        self.assertEqual(code, SynonymServiceResponse.Created)
        self.assertTrue(response['success'])
        self.assertEqual(1, Synonym.query.filter_by(synonym='brand').count())

    def test_add_synonym_multiple(self):
        """ Test that adding multiple synonym with the same snonym to a brand results in errors """
        brand = self._create_dummy_brand(self._create_dummy_account('account@example.com').id, 'Brand')

        add_synonym(brand.id, {'synonym': 'Brand'})
        response, code = add_synonym(brand.id, {'synonym': 'Brand'})

        self.assertEqual(code, SynonymServiceResponse.AlreadyExists)
        self.assertFalse(response['success'])

    def test_delete_synonym_multiple_brands(self):
        """ Test that deleting a synonym used by multiple brands does not remove the synonym if one still has it """
        accounts, brands, synonyms = self._create_n_associations(2, 'Brand')

        response, code = delete_synonym(brands[0].id, 'brand')

        self.assertEqual(code, SynonymServiceResponse.Success)
        self.assertTrue(response['success'])

        # There should still be one association in the data
        self.assertEqual(BrandSynonym.query.count(), 1)

        # Additionally, the synonym should still be in the database
        self.assertEqual(Synonym.query.count(), 1)

    def test_delete_synonyms_multiple_brands(self):
        """ Test that deleting a synonym for all brands using it removes the synonym """
        accounts, brands, synonyms = self._create_n_associations(2, 'Brand')

        delete_synonym(brands[0].id, 'brand')
        delete_synonym(brands[1].id, 'brand')

        # There should be no associations left
        self.assertEqual(BrandSynonym.query.count(), 0)

        # The synonym should still be in the database (as an inactive synonym)
        self.assertEqual(Synonym.query.count(), 1)

    def test_add_same_synonym_multiple_brands(self):
        """ Test that adding the same synonym to multiple brands results in only one synonym """
        first_account = self._create_dummy_account('first@example.com')

        first_brand = self._create_dummy_brand(first_account.id, 'First')
        second_brand = self._create_dummy_brand(first_account.id, 'Second')

        add_synonym(first_brand.id, {'synonym': 'Example'})
        add_synonym(second_brand.id, {'synonym': 'Example'})

        self.assertEqual(1, Synonym.query.filter_by(synonym='example').count())

    def test_get_brand_synonyms(self):
        """ Test that retrieving synonyms from a brand works """
        accounts, brands, synonym = self._create_n_associations(1, 'Brand')

        self.assertEqual(set(get_brand_synonyms(brands[0].id)), {synonym})

    def test_preprocess_synonym(self):
        """ Test that pre-processing of a synonym returns a pre-processed synonym """
        self.assertEqual('brand', preprocess_synonym('Brand'))

    def test_get_active_synonyms(self):
        """ Test that multiple brands with the same synonym has the correct count in active synonyms """
        self._create_n_associations(4, 'Brand')

        synonyms = dict(get_active_synonyms())
        self.assertIn('brand', synonyms)
        self.assertEqual(synonyms['brand'], 4)


if __name__ == "__main__":
    unittest.main()
