""" Data representation - Routines for user to interact with the API.

    Attributes:
        ORDER_COUNT (int) - Global variable holds count of food orders

        ALL_FOOD_ORDERS (dict) - Global variable holds all food orders
            {order_id(int):
                {'user_tel': str,
                'username': str,
                'order_qty': int,
                'order_description': str,
                'order_datetime': str,
                'order_accept_status': bool
                'user_location': 'str'
                }
            }
"""

import datetime
from flask_restful import Resource

ALL_FOOD_ORDERS = {}
ORDER_COUNT = 1


class FoodOrders(Resource):
    """ Holds methods to display all and create food orders """
    def get(self):
        """Fetch all Food Orders

        Returns a dictionary with all food orders or descriptive message if no
        orders have been placed yet.
        ---
        tags:
          - Fetch all / Create a Food order
        responses:
          200:
            description: All available food orders
          404:
            description: Bad user request
        """
        if ALL_FOOD_ORDERS == {}:
            msg_out = {"Dear customer": "No food orders placed yet"}
        else:
            msg_out = ALL_FOOD_ORDERS
        return msg_out

    def post(self, order_request_info):
        """Creates a new food order with provided <order_request_info>.

        Returns a dictionary with descriptive message to user indicating
        opertation status, success, failure or error message

        ---
        tags:
          - Fetch all / Create a Food order
        parameters:
          - in: body
            name: order_request_info
            type: object
            required: true
            description: Dictionary containing food order details
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
        global ALL_FOOD_ORDERS, ORDER_COUNT

        if isinstance(order_request_info, dict):
            # Expected keys in input dict
            chklst = [
                "username", "user_tel", "order_qty",
                "order_description", "user_location"
            ]
            # check for expected keys in input dict
            if set(
                    [True for _ in chklst if _ in order_request_info]
                ) == {True}:
                order_request_info['order_datetime'] = \
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                order_request_info['order_accept_status'] = False

                ALL_FOOD_ORDERS[ORDER_COUNT] = order_request_info
                ORDER_COUNT += 1
                msg_out = {"Success": "Order placed successully"}

            else:
                msg_out = {
                    "Invalid Input message":
                    "Order placement failed ... missing information"
                }
        else:
            msg_out = {
                "Invalid Input message": "Argument should be a dictionary"
            }

        return msg_out


class FoodOrderOps(Resource):
    """ Holds methods for operations on individual(by orderID) food orders """
    def get(self, order_id):
        """ Fetch a food order by order ID

        Returns a dictionary with food order corresponding to <orderid>
        or a descriptive error message to user
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
        try:
            int(order_id)
            if order_id > 0 and order_id in ALL_FOOD_ORDERS:
                msg_out = ALL_FOOD_ORDERS[order_id]
            else:
                msg_out = {
                    "Order fetching error message": "orderid out of range"
                }
        except ValueError:
            msg_out = {
                "Order fetching error message": "orderid should be integer"
            }
        finally:
            return msg_out

    def put(self, order_id, order_status):
        """ Change Food order status

            Returns a dictionary with a custom message to user to indicate
            order acceptance update Success or failure.
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
        if isinstance(order_id, int) and isinstance(order_status, bool):
            if order_id in ALL_FOOD_ORDERS:
                ALL_FOOD_ORDERS[order_id]['order_accept_status'] =\
                    order_status
                msg_out = {"Order status message": "Update Successful"}
            else:
                msg_out = {"Order status message": "orderid out of range"}
        else:
            msg_out = {"Order update error message": "Invalid Input"}

        return msg_out


if __name__ == '__main__':
    pass
