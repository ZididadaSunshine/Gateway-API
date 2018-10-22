import os

from peewee import SqliteDatabase

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'not-so-secret')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = SqliteDatabase('development.db')


class ProductionConfig(Config):
    DEBUG = False


configurations = dict(dev=DevelopmentConfig,
                      prod=ProductionConfig)
