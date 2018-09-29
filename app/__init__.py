""" Initialization file - App factory"""
import os
from flask import Flask, jsonify
from flasgger import Swagger
from app.api.v1.models import FoodOrders, FoodOrderOps
from instance.config import app_config

# Custom error handlers
def page_not_found(err):
    """ 404 status custom return message """
    return jsonify("Sorry... The page youre are looking for does not exist"), 404

def bad_user_request(err):
    """ 404 status custom return message """
    return jsonify("Sorry... Bad user request"), 400


def create_app(config_mode):
    """ Init the app """
    app = Flask(__name__, instance_relative_config=True)
    swagger = Swagger(app)  # Documentation
    app.config.from_object(app_config[config_mode])
    app.config.from_pyfile('config.py')  # config file
    from app.api.v1 import views  # load views
    # Register Blueprints
    app.register_blueprint(views.v1_bp)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(400, bad_user_request)

    return app