import unittest

from app.main.service.synonym_service import get_active_synonyms
from test.base.database_testcase import DatabaseTestCase


class SynonymServiceTests(DatabaseTestCase):
    def _create_n_associations(self, count, brand_name):
        """ Creates n accounts, n brands and n associations where all brands share the same synonym """
        synonym = self._create_dummy_synonym(brand_name)

        accounts = [self._create_dummy_account(f'account{n}@example.com') for n in range(count)]
        brands = [self._create_dummy_brand(accounts[n].id, brand_name) for n in range(count)]
        associations = [self._create_dummy_association(brands[n].id, synonym.id) for n in range(count)]

        return accounts, brands, associations

    def test_get_active_synonyms(self):
        """ Test that two brands with the same synonym has the correct count in active synonyms """
        self._create_n_associations(4, 'Brand')

        synonyms = dict(get_active_synonyms())
        self.assertIn('Brand', synonyms)
        self.assertEqual(synonyms['Brand'], 4)


if __name__ == "__main__":
    unittest.main()
