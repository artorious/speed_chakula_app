""" Defines the base routes for app """
from flask import Blueprint, jsonify, make_response


v2_base_bp = Blueprint('v2_base', __name__, url_prefix='/api/v2')


@v2_base_bp.route('/', methods=['GET'])
def index():
    """ Homepage. Returns welcome message """
    return make_response(jsonify(
        "Welcome User. Speedy Chakula delivers fast-food-fast"
    )), 200
