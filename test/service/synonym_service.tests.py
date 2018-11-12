from test.base.database_testcase import DatabaseTestCase


class SynonymServiceTests(DatabaseTestCase):
    def test_get_active_synonyms(self):
        first_account = self._create_dummy_account('first@example.com')
        second_account = self._create_dummy_account('first@example.com')