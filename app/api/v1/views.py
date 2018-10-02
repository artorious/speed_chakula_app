""" Defines routes for app """

from flask import Blueprint, jsonify, request
from app.api.v1.models import FoodOrders, FoodOrderOps

v1_bp = Blueprint('v1_base', __name__, url_prefix='/api/v1')

ALL_ORDERS = FoodOrders()
ORDER_OPS = FoodOrderOps()


@v1_bp.route('/', methods=['GET'])
def index():
    """ Homepage. Returns welcome message 
    ---
        tags:
          - Home page
        responses:
          200:
            description: Success
          404:
            description: Bad user request
    """
    return jsonify("Welcome User. Speedy Chakula delivers fast-food-fast")


@v1_bp.route('/orders', methods=['GET'])
def fetch():
    """ Fetch all food orders. Returns a dictionary of food orders.
    ---
        tags:
          - Fetch all Food orders
        responses:
          200:
            description: All available food orders
          404:
            description: Bad user request
     """
    return jsonify(ALL_ORDERS.get())


@v1_bp.route('/orders', methods=['POST'])
def create():
    """ Create a new food order.
    ---
        tags:
          -Create a Food order
        parameters:
          - in: body
            name: order_request_info
            type: object
            required: true
            description: Dictionary containing food order details
            requestBody:
                
        responses:
          200:
            description: "Success"
          201:
            description: "Order placed successully"
          400:
            description: "Bad Request"
          404:
            description: "Resource not found"

    """
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
    '/orders/<int:orderid>', methods=['GET']
)
def fetch_order_by_id(orderid):
    """ Fetch food order by id. 
    ---
        tags:
          - Operations on Food orders
        parameters:
          - in: path
            name: orderid
            description: The ID of the food order, try 1!
            type: integer
            required: true
        responses:
          200:
            description: Requested food orders
          404:
            description: Bad user request
        
    """
    if isinstance(orderid, int):
            msg_out = jsonify(ORDER_OPS.get(orderid))
    else:
        msg_out = jsonify(
            {"Order fetching error message": "orderid should be integer"}
            )
    return msg_out


@v1_bp.route(
    '/orders/<int:orderid>', methods=['PUT']
)
def change_order_status(orderid):
    """  Change food order status True/False 
    ---
        tags:
          - Operations on Food orders
        parameters:
          - in: path
            name: orderid
            required: true
            description: The ID of the Food ordertask, try 1!
            type: integer
          - in: body
            name: order_status
            type: boolean
            required: true
        responses:
          200:
            description: "Order status updated succesfully"
          400:
            description: "Bad Request"
          404:
            description: "Resource not found"
    """
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

