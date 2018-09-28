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
app.register_blueprint(views_v1.v1_bp)
app.register_blueprint(views_v2.v2_base_bp)
app.register_blueprint(views_v2.v2_auth_bp)

# Add API resources
api.add_resource(FoodOrders, '/orders')
api.add_resource(FoodOrderOps, '/orders/<orderid>')
api.add_resource(SignUp, '/signup')