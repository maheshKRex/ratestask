import os

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    ENV = "production"
    CSRF_ENABLED = True

class DevConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    ENV = "test"
    TESTING = True