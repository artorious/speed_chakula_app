""" Defines routes for app """

from flask import Blueprint, jsonify, request
from app.api.v2.models import SignUp
from app import create_app

v2_base_bp = Blueprint('v2_base', __name__, url_prefix='/api/v2')
v2_auth_bp = Blueprint('v2_auth', __name__, url_prefix='/api/v2/auth')

@v2_base_bp.route('/', methods=['GET'])
def index():
    """ Homepage. Returns welcome message """
    return 

@v2_auth_bp.route('/signup', methods=['GET'])
def signup():
    """ Register new user """
    pass