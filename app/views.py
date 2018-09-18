""" Defines routes for app """

from flask import request
from flask import jsonify
from app.models import FoodOrders, FoodOrderOps
from app import app


@app.route('/route_name')
def index():
    """ Homepage. Returns welcome message """
    return

@app.route('/api/v1/orders', methods=['GET', 'POST'])
def orders():
    """ Fetch all food orders or create a new food order """
    return

@app.route('/api/v1/orders/<int:orderid>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def order_by_id():
    return
