""" Project configuration variables """
from os import getenv

class Config():
    """ General Config. """
    DEBUG = False
    SECRET = getenv('SECRET')
    APP_SETTINGS = getenv("APP_SETTINGS")

class DevConfig(Config):
    """ Development Config. """
    DEVELOPMENT = True
    DEBUG = True
    DATABASE_URL = getenv(DATABASE_URL)


class TestingConfig(Config):
    """ Testing configs """
    TESTING = True
    DATABASE_URL = getenv(TEST_DATABASE_URL)


app_config = {
    'development': DevConfig,
    'testing': TestingConfig
}
