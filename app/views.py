""" Defines routes for app """

from flask import request
from flask import jsonify
from app.models import FoodOrders
from app import app


SAMPLE_FOOD_ORDERS = FoodOrders()


@app.route('/api/v1/orders', methods=['GET'])
def fetch_all_orders():
    """ Fetches all food orders """
    return jsonify(SAMPLE_FOOD_ORDERS.all_food_orders)


@app.route('/api/v1/orders', methods=['POST'])
def place_new_order():
    """ Creates a new food order """
    req_data = request.get_json()

    if (
            'username' in req_data and
            'user_tel' in req_data and
            'order_qty' in req_data and
            'order_description' in req_data and
            'user_location' in req_data
    ):
        return jsonify(SAMPLE_FOOD_ORDERS.place_new_order(req_data))
    return jsonify('Sorry.... Order placement Failed')


@app.route('/api/v1/orders/<int:orderid>', methods=['GET'])
def fetch_order_by_id(orderid):
    """ Fetches a single food order matching the provided <orderid>"""
    if isinstance(orderid, int):
        return jsonify(SAMPLE_FOOD_ORDERS.fetch_order_by_id(orderid))
    return jsonify(
        {"Order fetching error message": "orderid should be integer"}
    )


@app.route('/api/v1/orders/<int:orderid>', methods=['PUT'])
def update_order_by_id(orderid):
    """ Updates a single food order matching the provided <orderid> """
    req_data = request.get_json()

    if isinstance(orderid, int) and isinstance(req_data, bool):
        return jsonify(
            SAMPLE_FOOD_ORDERS.update_order_by_id(orderid, req_data)
        )
    return jsonify({"Order update message": "Update Failed..Invalid input"})
