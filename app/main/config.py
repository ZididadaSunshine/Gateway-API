import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'not-so-secret')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_REQUEST_DURATION = True


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "development.db")}'


class TestingConfig(Config):
    ENV = 'test'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "test.db")}'


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "production.db")}'


configurations = dict(dev=DevelopmentConfig,
                      prod=ProductionConfig,
                      test=TestingConfig)

secret = Config.SECRET_KEY
