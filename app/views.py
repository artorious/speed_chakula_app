""" Defines routes for app """

from flask import request
from flask import jsonify
from app.models import FoodOrders
from app import app


sample_food_offers = FoodOrders()


@app.route('/api/v1/orders', methods=['GET'])
def fetch_all_orders():
    """ Fetches all food orders """
    return jsonify(sample_food_offers.all_food_orders)
