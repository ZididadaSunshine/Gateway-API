from flask_testing import TestCase

from app import blueprint
from app.main import create_app


class BaseTestCase(TestCase):
    @staticmethod
    def get_sample_brand():
        return dict(name='Aalborg University')

    @staticmethod
    def get_sample_account():
        # Returned in a function in order to make it immutable
        return dict(email='test@example.com', first_name='Test', last_name='Account', password='example')

    @staticmethod
    def get_sample_credentials():
        return dict(email='test@example.com', password='example')

    def create_app(self):
        app = create_app('test')

        app.register_blueprint(blueprint)

        return app
