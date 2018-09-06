""" Test cases for models.py """

import unittest
from app.models import FoodOrders


class TestFoodOrders(unittest.TestCase):
    """ Test FoodOrders class """

    def setUp(self):
        """ Instantiate """
        self.sample_food_orders = FoodOrders()
        self.sample_order_request_info = {
            "username": "mrnoname",
            "order_qty": 2,
            "order_description": "500ml soda @Ksh. 100/="
        }

    def test_class_inits_with_dict(self):
        """ Test class inits with a dict """
        self.assertIsInstance(
            self.sample_food_orders.all_food_orders, dict,
            msg='Class does not initialize with a dict'
        )

    def test_class_inits_with_an_order_count_var(self):
        """ Test class inits with an order count variable to"""
        self.assertIsInstance(
            self.sample_food_orders.food_order_count, int,
            msg="Class does not initialize with a valid order coount"
        )

    def test_fetch_all_food_orders_return_value(self):
        """ Test that fetch_all_food_orders() returns a dictionary """
        self.assertIsInstance(
            self.sample_food_orders.fetch_all_food_orders(), dict,
            msg="Method should return a dict"
        )

    def test_place_new_order_only_accepts_valid_data(self):
        """ Tests handling of invalid input/datatype.
            Raises TypeError and return custom error message
        """
        self.assertRaises(
            TypeError, self.sample_food_orders.place_new_order, 1,
            "Argument should be a dictionary"
        )

        self.assertIn(
            "Order placement message",
            self.sample_food_orders.place_new_order(
                self.sample_order_request_info
            )
        )

    def test_fetch_one_order_returns_dict(self):
        """ Test that fetch_one_order() returns dict with details """
        pass

    def test_fetch_one_order_handles_out_of_range_orderid(self):
        """ Test that out of range orderId return custom error message 
            (Out of range)
        """

    def test_fetch_one_order_with_non_int_orderid(self):
        """ Test that invalid (non-int) orderId returns custom error message
            (only positive int)
        """
        pass


if __name__ == '__main__':
    unittest.main()
