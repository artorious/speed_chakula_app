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
    else:
        return jsonify('Sorry.... Order placement Failed')

@app.route('/api/v1/orders/<int:orderID>', methods=['GET'])
def fetch_order_by_id(orderId):
    """ Fetches a single food order corresponding to the provided <orderID>"""
    return