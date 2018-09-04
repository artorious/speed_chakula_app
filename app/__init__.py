""" Initialization file """

from flask import Flask


# Init the app
app = Flask(__name__, instance_relative_config=True)

# load views
from app import views

# Load the config file
app.config.from_object('config')
