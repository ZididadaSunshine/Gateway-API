import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'not-so-secret')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_REQUEST_DURATION = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "development.db")}'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "production.db")}'


configurations = dict(dev=DevelopmentConfig,
                      prod=ProductionConfig)

secret = Config.SECRET_KEY
