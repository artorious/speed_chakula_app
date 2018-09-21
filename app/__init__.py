""" Initialization file """
import os
from flask import Flask

# Init the app
app = Flask(__name__, instance_relative_config=True)


# Load the config file
app.config.from_object('instance.config')


# load views
from app.api.v1 import views

app.register_blueprint(views.v1_bp)

 

