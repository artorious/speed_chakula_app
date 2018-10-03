""" Initialization file - App factory"""
import os
from flask import Flask, jsonify
from flasgger import Swagger
from instance.config import app_config

# Custom error handlers
def page_not_found(err):
    """ 404 status custom return message """
    return jsonify("Sorry... The page youre are looking for does not exist"), 404

def bad_user_request(err):
    """ 400 status custom return message """
    return jsonify("Sorry... Bad user request"), 400

def server_side_error(err):
    """ 500 status custom return message """
    return jsonify("Sorry... Internal Server error"), 500



def create_app(config_mode):
    """ Init the app """
    app = Flask(__name__, instance_relative_config=True)
    swagger = Swagger(app)  # V1 Documentation on flasgger
    # config file loading
    app.config.from_object(app_config[config_mode])  
    from app.api.v1 import views as views_v1
    from app.api.v2 import views as views_v2

    # Register Blueprints
    app.register_blueprint(views_v1.v1_bp)
    app.register_blueprint(views_v2.v2_base_bp)
    app.register_blueprint(views_v2.v2_auth_bp)
    # Custom error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(400, bad_user_request)
    app.register_error_handler(500, server_side_error)

    return app
