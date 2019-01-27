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
    BASE_API_ENDPOINT = "http://api:5000/api"


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    BASE_API_ENDPOINT = "http://127.0.0.1:5002/api"


class TestingConfig(Config):
    TESTING = True
    ENV = "testing"


ENVIRONMENTS = {
    ConfigEnum.Development: DevelopmentConfig,
    ConfigEnum.Staging: StagingConfig,
    ConfigEnum.Testing: TestingConfig,
    ConfigEnum.Production: ProductionConfig,
}
