""" Initialization file """
import os
from flask import Flask
from flasgger import Swagger
from flask_restful import Api, Resource
from app.api.v1.models import FoodOrders, FoodOrderOps
from app.api.v2.models import SignUp


# Init the app
app = Flask(__name__, instance_relative_config=True)
api = Api(app)

# Documentation
swagger = Swagger(app)

# Load the config file
app.config.from_object('instance.config')


# load views
from app.api.v1 import views as views_v1
from app.api.v2 import views as views_v2

# Register Blueprints
""" Test cases for views.py """

import unittest
import json
from app import app

# Add API resources
api.add_resource(FoodOrders, '/orders')
api.add_resource(FoodOrderOps, '/orders/<orderid>')
api.add_resource(SignUp, '/signup')