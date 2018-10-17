import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'not-so-secret')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir)}main.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


configurations = dict(dev=DevelopmentConfig,
                      prod=ProductionConfig)
