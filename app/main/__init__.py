from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from app.main.config import configurations

# Initialize SQLAlchemy database
database = SQLAlchemy()

# Initialzie Bcrypt
bcrypt = Bcrypt()


def create_app(config):
    # Check if configuration is valid
    if config not in configurations:
        raise ValueError(f'{config} is not a valid configuration.')

    # Create Flask application and initialize Bcrypt and SQLAlchemy with the application instance
    app = Flask(__name__)
    app.config.from_object(configurations[config])
    database.init_app(app)
    bcrypt.init_app(app)

    return app
