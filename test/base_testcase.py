from flask_testing import TestCase

from app import blueprint
from app.main import create_app


class BaseTestCase(TestCase):
    AccountSample = dict(email='test@example.com', first_name='Test', last_name='Account', password='example')

    def create_app(self):
        app = create_app('test')

        app.register_blueprint(blueprint)

        return app
