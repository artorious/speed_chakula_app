""" Data representation - holds routines for user to interact with the API."""


class FoodOrders():
    """ Holds methods for food orders

        Attributes:
            all_food_orders (dict) - Variable holds all food orders
                {order_count(int): 
                    {'orderID': int,
                    'username': str,
                    'order_qty': int,
                    'order_description': str,
                    'order_datetime': str,
                    'order_status': bool
                    }
                }
    """

    def __init__(self):
        self.all_food_orders = {}

    def fetch_all_food_orders(self):
        """ (FoodOrders) -> dict

            Fetches all food orders. Returns a dict.
        """
        return self.all_food_orders
