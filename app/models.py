""" Data representation - holds routines for user to interact with the API."""

import datetime


class FoodOrders():
    """ Holds methods for food orders

        Attributes:
            all_food_orders (dict) - Variable holds all food orders
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

    def __init__(self):
        self.all_food_orders = {}
        self.food_order_count = 1

    def fetch_all_food_orders(self):
        """ (FoodOrders) -> dict

            Fetches all food orders. Returns a dict.
        """
        return self.all_food_orders

    def place_new_order(self, order_request_info):
        """ (FoodOrders, dict) -> dict

            Creates a new food order with provided <order_info>.
            Returns message to user on creation or failure
        """
        if isinstance(order_request_info, dict):
            order_request_info['order_datetime'] = \
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            order_request_info['order_accept_status'] = False
            self.all_food_orders[self.food_order_count] = order_request_info
            self.food_order_count += 1

            return {"Order placement message": "Order succesfully placed"}
        else:
            raise TypeError("Argument should be a dictionary")

    def fetch_order_by_id(self, orderid):
        """ (FoodOrders, int) -> dict

            Returns food order with corresponding orderid
        """
        try:
            int(orderid)
            if orderid in self.all_food_orders:
                return self.all_food_orders[orderid]
            else:
                return {"Order fetching error message": "orderid out of range"}
        except ValueError:
            return {
                "Order fetching error message": "orderid should be integer"
            }

    def update_order_by_id(self, orderid, update_status):
        """ (FoodOrders, int, bool) -> dict

            Returns custom message to user to indicat update status
        """
        if isinstance(orderid, int) and isinstance(update_status, bool):
            if orderid in self.all_food_orders:
                self.all_food_orders[orderid]['order_accept_status'] =\
                    update_status
                return {"Order update message": "Update Successful"}
            return {"Order update error message": "orderid out of range"}
        return {
                "Order update error message": "Invalid Input"
            }


if __name__ == '__main__':
    FoodOrders()
