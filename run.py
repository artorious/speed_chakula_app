""" Application root. Run first to start server and launch app """

from os import getenv
from app import create_app


config_mode = getenv('APP_SETTINGS')
app = create_app(config_mode)

if __name__ == '__main__':
    app.run()
