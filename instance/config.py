""" Project configuration variables """
import os

class Config():
    """ General Config. """
    DEBUG = False
    SECRET = os.getenv('SECRET')

class DevConfig(Config):
    """ Development Config. """
    DEBUG = True
    

app_config = {'development': DevConfig}