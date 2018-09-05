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
    return
