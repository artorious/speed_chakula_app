""" Initialization file """
import os
from flask import Flask
from flasgger import Swagger
from flask_restful import Api, Resource
from app.api.v1.models import FoodOrders, FoodOrderOps


# Init the app
app = Flask(__name__, instance_relative_config=True)
api = Api(app)

# Documentation
swagger = Swagger(app)

# Load the config file
app.config.from_object('instance.config')


# load views
from app.api.v1 import views

# Register Blueprints
app.register_blueprint(views.v1_bp)

# Add API resources
api.add_resource(FoodOrders, '/orders')
api.add_resource(FoodOrderOps, '/orders/<orderid>')
