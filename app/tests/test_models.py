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
            msg="Class does not initialize with a valid order count"
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
        """ Test that fetch_order_by_id(orderid) returns dict """
        self.sample_food_orders.place_new_order(
            self.sample_order_request_info
        )

        self.assertIsInstance(
            self.sample_food_orders.fetch_order_by_id(1),
            dict,
            msg='Method does not return a dict'
        )

    def test_fetch_one_order_handles_out_of_range_orderid(self):
        """ Test that out of range orderid return custom error message
            (Out of range)
        """
        self.sample_food_orders.place_new_order(
            self.sample_order_request_info
        )

        self.assertDictEqual(
            self.sample_food_orders.fetch_order_by_id(2),
            {"Order fetching error message": "orderid out of range"},
            msg="Method does not handle out of range orders"
        )

        self.assertDictEqual(
            self.sample_food_orders.fetch_order_by_id(2),
            {"Order fetching error message": "orderid out of range"},
            msg="Method does not handle out of range orders"
        )

    def test_fetch_one_order_with_non_int_orderid(self):
        """ Test that invalid (non-int) orderid returns custom error message
            (only positive int)
        """
        self.sample_food_orders.place_new_order(
            self.sample_order_request_info
        )

        self.assertDictEqual(
            self.sample_food_orders.fetch_order_by_id('2.0'),
            {"Order fetching error message": "orderid should be integer"},
            msg="Method does not handle non-integers for orderid"
        )

        self.assertDictEqual(
            self.sample_food_orders.fetch_order_by_id('one'),
            {"Order fetching error message": "orderid should be integer"},
            msg="Method does not handle non-integers for orderid"
        )

    def test_update_order_returns_dict(self):
        """ Test that update_order_by_id(orderid) returns dict """
        self.sample_food_orders.place_new_order(
            self.sample_order_request_info
        )

        self.assertIsInstance(
            self.sample_food_orders.update_order_by_id(1, True),
            dict,
            msg='Method does not return a dict'
        )
    
    def test_update_order_handles_out_of_range_orderid(self):
        """ Test that out of range orderid return custom error message
            (Out of range)
        """
        self.sample_food_orders.place_new_order(
            self.sample_order_request_info
        )

        self.assertDictEqual(
            self.sample_food_orders.update_order_by_id(2, True),
            {"Order update error message": "orderid out of range"},
            msg="Method does not handle out of range orders"
        )

        self.assertDictEqual(
            self.sample_food_orders.update_order_by_id(0, True),
            {"Order update error message": "orderid out of range"},
            msg="Method does not handle out of range orders"
        )

    def test_update_order_handles_invalid_input(self):
        """ Test that invalid (non-int) orderid and update_status (non-bool)
            returns custom error message    
        """
        self.sample_food_orders.place_new_order(
            self.sample_order_request_info
        )

        self.assertDictEqual(
            self.sample_food_orders.update_order_by_id('2.0', True),
            {"Order update error message": "Invalid Input"},
            msg="Method does not handle non-integers for orderid"
        )

        self.assertDictEqual(
            self.sample_food_orders.update_order_by_id(1, "True"),
            {"Order update error message": "Invalid Input"},
            msg="Method does not handle non-integers for orderid"
        )


if __name__ == '__main__':
    unittest.main()
