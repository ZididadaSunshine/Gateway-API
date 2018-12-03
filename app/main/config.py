import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'not-so-secret')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_REQUEST_DURATION = True
    API_KEY = os.getenv('API_KEY', 'secret')


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("DB_GATEWAY_USERNAME", None)}:{os.getenv("DB_GATEWAY_PASSWORD", None)}@{os.getenv("DB_GATEWAY_HOST", None)}/{os.getenv("DB_GATEWAY_DATABASE", None)}_dev'


class TestingConfig(Config):
    ENV = 'test'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("DB_GATEWAY_USERNAME", None)}:{os.getenv("DB_GATEWAY_PASSWORD", None)}@{os.getenv("DB_GATEWAY_HOST", None)}/{os.getenv("DB_GATEWAY_DATABASE", None)}_test'


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("DB_USERNAME", None)}:{os.getenv("DB_PASSWORD", None)}@{os.getenv("DB_HOST", None)}/{os.getenv("DB_DATABASE", None)}'


configurations = dict(dev=DevelopmentConfig,
                      prod=ProductionConfig,
                      test=TestingConfig)

secret = Config.SECRET_KEY
