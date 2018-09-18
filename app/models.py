""" Data representation - Routines for user to interact with the API.
    
    Attributes:
        ORDER_COUNT (int) - Global variable holds count of food orders

        ALL_FOOD_ORDERS (dict) - Global variable holds all food orders
            {order_count(int):
                {'orderid': int,
                'username': str,
                'order_qty': int,
                'order_description': str,
                'order_datetime': str,
                'order_accept_status': bool
                }
            }      
"""

import datetime
 
# GLOBAL Var to hold all food orders
# GLobal var to hold counter

class FoodOrders():
    """ Holds methods to display all and create food orders """
    def __init__(self):
        pass
    
    def get(self):
        """ (FoodOrders) -> dict

            Returns a dictionary with all food orders or descriptive message
            if no orders have been placed yet.
        """
        return

    def post(self, order_request_info):
        """ (FoodOrders, dict) -> dict

            Creates a new food order with provided <order_request_info>.
            Returns a dictionary with descriptive message to user indicating
            opertation status, success, failure or error message
        """
        return

class FoodOrderOps():
    """ Holds methods for operations on individual(by orderID) food orders """
    def __init__(self):
        pass

    def get(self, order_id):
        """ (FoodOrderOps, int) -> dict

            Returns a dictionary with food order corresponding to <orderid>
            or a descriptive error message to user
        """
        return

    def put(self, order_id, order_status):
        """ (FoodOrderOps, int, bool) -> dict

            Returns a dictionary with a custom message to user to indicate 
            order acceptance update Success or failure.
        """
        return
    
    #TODO:
    def patch(self, order_id, food_order_changes):
        """ update food order by <order_id> with <food_order_changes> """
        pass

    def delete(self, order_id):
        """ delete food order by <order_id> """
        pass


if __name__ == '__main__':
    pass
