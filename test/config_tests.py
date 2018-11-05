import unittest

from flask_testing import TestCase

from app.main import create_app


class TestConfigTests(TestCase):
    def create_app(self):
        return create_app('test')

    def test_env(self):
        self.assertEqual(self.app.config['ENV'], 'test')

    def test_testing(self):
        self.assertEqual(self.app.config['TESTING'], True)

    def test_debug(self):
        self.assertEqual(self.app.config['DEBUG'], True)

    def test_database_uri(self):
        self.assertIn('test.db', self.app.config['SQLALCHEMY_DATABASE_URI'])


class ProductionConfigTests(TestCase):
    def create_app(self):
        return create_app('prod')

    def test_env(self):
        self.assertEqual(self.app.config['ENV'], 'production')

    def test_testing(self):
        self.assertEqual(self.app.config['TESTING'], False)

    def test_debug(self):
        self.assertEqual(self.app.config['DEBUG'], False)

    def test_database_uri(self):
        self.assertIn('production.db', self.app.config['SQLALCHEMY_DATABASE_URI'])


class DevelopmentConfigTests(TestCase):
    def create_app(self):
        return create_app('dev')

    def test_env(self):
        self.assertEqual(self.app.config['ENV'], 'development')

    def test_testing(self):
        self.assertEqual(self.app.config['TESTING'], False)

    def test_debug(self):
        self.assertEqual(self.app.config['DEBUG'], True)

    def test_database_uri(self):
        self.assertIn('development.db', self.app.config['SQLALCHEMY_DATABASE_URI'])





if __name__ == "__main__":
    unittest.main()
