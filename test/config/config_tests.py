import unittest

from app.main import create_app
from test.base.base_testcase import BaseTestCase


class TestConfigTests(BaseTestCase):
    def create_app(self):
        return create_app('test')

    def test_env(self):
        """ Test the environment variable of the test environment """
        self.assertEqual(self.app.config['ENV'], 'test')

    def test_testing(self):
        """ Test the testing variable of the test environment """
        self.assertEqual(self.app.config['TESTING'], True)

    def test_debug(self):
        """ Test the debug variable of the test environment """
        self.assertEqual(self.app.config['DEBUG'], True)

    def test_database_uri(self):
        """ Test the database variable of the test environment """
        self.assertTrue('postgresql', self.app.config['SQLALCHEMY_DATABASE_URI'])


class ProductionConfigTests(BaseTestCase):
    def create_app(self):
        return create_app('prod')

    def test_env(self):
        """ Test the environment variable of the production environment """
        self.assertEqual(self.app.config['ENV'], 'production')

    def test_testing(self):
        """ Test the testing variable of the production environment """
        self.assertEqual(self.app.config['TESTING'], False)

    def test_debug(self):
        """ Test the debug variable of the production environment """
        self.assertEqual(self.app.config['DEBUG'], False)

    def test_database_uri(self):
        """ Test the database variable of the production environment """
        self.assertTrue('postgresql', self.app.config['SQLALCHEMY_DATABASE_URI'])


class DevelopmentConfigTests(BaseTestCase):
    def create_app(self):
        return create_app('dev')

    def test_env(self):
        """ Test the environment variable of the development environment """
        self.assertEqual(self.app.config['ENV'], 'development')

    def test_testing(self):
        """ Test the testing variable of the development environment """
        self.assertEqual(self.app.config['TESTING'], False)

    def test_debug(self):
        """ Test the debug variable of the development environment """
        self.assertEqual(self.app.config['DEBUG'], True)

    def test_database_uri(self):
        """ Test the database variable of the development environment """
        self.assertIn('development.db', self.app.config['SQLALCHEMY_DATABASE_URI'])


if __name__ == "__main__":
    unittest.main()
