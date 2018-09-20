""" Defines routes for app """

from flask import request
from flask import jsonify
from app.models import FoodOrders, FoodOrderOps
from app import app

ALL_ORDERS = FoodOrders()
ORDER_OPS = FoodOrderOps()


@app.route('/api/v1/', methods=['GET'])
def index():
    """ Homepage. Returns welcome message """
    return jsonify("Welcome User. Speedy Chakula delivers fast-food-fast")


@app.route('/api/v1/orders', methods=['GET', 'POST'])
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

@app.route(
    '/api/v1/orders/<int:orderid>', methods=['GET', 'PUT']
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
