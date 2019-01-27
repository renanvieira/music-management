import os
from enum import Enum

basedir = os.path.abspath(os.path.dirname(__file__))


class Application(object):
    pass


class ConfigEnum(Enum):
    Production = 'production'
    Staging = 'staging'
    Development = "development"
    Testing = 'testing'


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'RdDTA+yomt-~YQ~zk,!BGurrFJ~g6ba*'
    SQLALCHEMY_DATABASE_URI = "sqlite:///data/album_database.db"
    ITEMS_PER_PAGE = 10


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///data/album_database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///data/album_database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    ENV = "testing"
    SQLALCHEMY_DATABASE_URI = "sqlite:///data/album_database_test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 2


ENVIRONMENTS = {
    ConfigEnum.Development: DevelopmentConfig,
    ConfigEnum.Staging: StagingConfig,
    ConfigEnum.Testing: TestingConfig,
    ConfigEnum.Production: ProductionConfig,
}
