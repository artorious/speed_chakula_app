""" Defines routes for app """

from flask import Blueprint, jsonify, request
from app.api.v1.models import FoodOrders, FoodOrderOps
from app import app
# TODO: Blueprints
v1_bp = Blueprint('v1_base', __name__, url_prefix='/api/v1')

ALL_ORDERS = FoodOrders()
ORDER_OPS = FoodOrderOps()


@v1_bp.route('/', methods=['GET'])
def index():
    """ Homepage. Returns welcome message """
    return jsonify("Welcome User. Speedy Chakula delivers fast-food-fast")


@v1_bp.route('/orders', methods=['GET', 'POST'])
def orders():
    """ Fetch all food orders or create a new food order """
    if request.method == 'GET':
        return jsonify(ALL_ORDERS.get())
    
    elif request.method == 'POST':
        req_data = request.get_json(force=True)
        if (
                'username' in req_data and
                'user_tel' in req_data and
                'order_qty' in req_data and
                'order_description' in req_data and
                'user_location' in req_data
        ):
            return jsonify(ALL_ORDERS.post(req_data))
        return jsonify('Sorry.... Order placement Failed')

@v1_bp.route(
    '/orders/<int:orderid>', methods=['GET', 'PUT', 'PATCH']
)
def order_by_id(orderid):
    """ Operate on a food order by <orderid>

        Display food order, update order status, ...
    """
    if request.method == 'GET':
        if isinstance(orderid, int):
            return jsonify(ORDER_OPS.get(orderid))
        return jsonify(
            {"Order fetching error message": "orderid should be integer"}
        )
    
    elif request.method == 'PUT':
        req_data = request.get_json(force=True)

        if isinstance(orderid, int) and isinstance(req_data, bool):
            return jsonify(
                ORDER_OPS.put(orderid, req_data)
            )
        return jsonify({"Order update message": "Update Failed..Invalid input"})
    
    elif request.method == 'PATCH':
        return