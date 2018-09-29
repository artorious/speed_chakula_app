""" Project configuration variables """
# Enable Debugging

DEBUG = True
""" Project configuration variables """
import os

class Config():
    """ General Config. """
    DEBUG = False
    SECRET = os.getenv('SECRET')

class DevConfig(Config):
    """ Development Config. """
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    """ Testing configs """
    TESTING = True

app_config = {
    'development': DevConfig,
    'testing': TestingConfig
}
