""" Defines routes for app """

from flask import Blueprint, jsonify, request
from app.api.v1.models import FoodOrders, FoodOrderOps

v1_bp = Blueprint('v1_base', __name__, url_prefix='/api/v1')

ALL_ORDERS = FoodOrders()
ORDER_OPS = FoodOrderOps()


@v1_bp.route('/', methods=['GET'])
def index():
    """ Homepage. Returns welcome message """
    return jsonify("Welcome User. Speedy Chakula delivers fast-food-fast")


@v1_bp.route('/orders', methods=['GET', 'POST'])
def orders():
    """ Fetch all food orders (GET) or create a new food order (POST)
        Returns a dictionary of food orders.
     """
    if request.method == 'GET':
        msg_out = jsonify(ALL_ORDERS.get())
    elif request.method == 'POST':
        req_data = request.get_json(force=True)
        if (
                'username' in req_data and
                'user_tel' in req_data and
                'order_qty' in req_data and
                'order_description' in req_data and
                'user_location' in req_data
        ):
            msg_out = jsonify(ALL_ORDERS.post(req_data))
        else:
            msg_out = jsonify('Sorry.... Order placement Failed')
    return msg_out


@v1_bp.route(
    '/orders/<int:orderid>', methods=['GET', 'PUT', 'PATCH']
)
def order_by_id(orderid):
    """ Operate on a food order by <orderid>

        Display food order, update order status, ...
    """
    if request.method == 'GET':
        if isinstance(orderid, int):
            msg_out = jsonify(ORDER_OPS.get(orderid))
        else:
            msg_out = jsonify(
                {"Order fetching error message": "orderid should be integer"}
            )
    elif request.method == 'PUT':
        req_data = request.get_json(force=True)
        if isinstance(orderid, int) and isinstance(req_data, bool):
            msg_out = jsonify(
                ORDER_OPS.put(orderid, req_data)
            )
        else:
            msg_out = jsonify(
                {"Order update message": "Update Failed..Invalid input"}
            )
    return msg_out
