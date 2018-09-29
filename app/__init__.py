""" Initialization file - App factory"""
import os
from flask import Flask
from flasgger import Swagger
from app.api.v1.models import FoodOrders, FoodOrderOps
from instance.config import app_config



def create_app(config_mode):
    """ Init the app """
    app = Flask(__name__, instance_relative_config=True)
    swagger = Swagger(app)  # Documentation
    app.config.from_object(app_config[config_mode])
    app.config.from_pyfile('config.py')  # config file
    from app.api.v1 import views  # load views
    app.register_blueprint(views.v1_bp)  # Register Blueprints

    return app