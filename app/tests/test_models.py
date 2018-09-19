""" Test cases for models.py """

import unittest
from app.models import FoodOrders, FoodOrderOps

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
    
    def test_get_returns_dict(self):
        """ Tests that method returns a dictionary """
        self.assertIsInstance(
            self.sample_food_orders.get(),
            dict,
            msg="Expected a dictionary"
        )
    
    def test_get_returns_msg_when_dict_is_empty(self):
        """ Tests for a custom message when no orders have been placed """
        self.assertIn(
            "Dear customer",
            self.sample_food_orders.get(),
            msg="Expected custom message when food order list is empty"
        )
    
    def test_get_returns_dict_with_correct_format_when_orders_exist(self):
        """ Tests that returned dictionary contains expected data/info """
        test_data = self.sample_food_orders.post(self.sample_order_request_info)
        self.assertIn(
            "username", test_data, msg="username absent from food order"
        )
        self.assertIn(
            "order_qty", test_data, msg="Order Qty absent from food order"
        )
        self.assertIn(
            "user_tel", test_data, msg="user_tel absent from food order"
        )
        self.assertIn(
            "order_description", test_data, msg="username absent from food order"
        )
        self.assertIn(
            "order_datetime", test_data, msg="order_datetime absent from food order"
        )
        self.assertIn(
            "order_accept_status", test_data, msg="order_accept_status absent from food order"
        )
        self.assertIn(
            "user_location", test_data, msg="user_location absent from food order"
        )
    
    def test_post_only_accepts_dicts_as_input(self):
        """ Tests handling of invalid input/datatype."""
        self.assertRaises(
            TypeError, self.sample_food_orders.post, 1,
        )
 
    def test_post_error_msg_on_invalid_input(self):
        """ 
            Tests for custom error message on method is calleed 
            with invalid data 
        """
        self.assertIn(
            "Invalid Input message",
            self.sample_food_orders.post("I want everything")
        )

    # def test_post_only_accepts_populated_dict_of_correct_format(self):
    #     pass

    def test_post_returns_operation_msg_to_user(self):
        """ Test for custom message to user on sucessful operation """
        self.assertIn(
            "Success",
            self.sample_food_orders.post(self.sample_order_request_info),
            msg="Order not created succesfully"
        )
    
    def tearDown(self):
        pass

class TestFoodOrdersOps(unittest.TestCase):
    """ Test FoodOrdersOps class """
    
    def setUp(self):
        """ Instantiate """
        self.sample_food_orders = FoodOrderOps()
        self.sample_order_request_info = {
            "username": "mrnoname",
            "order_qty": 2,
            "order_description": "500ml soda @Ksh. 100/="
        }
    
    def test_get_returns_dict_of_correct_format(self):
        """ Test that get(orderid) returns dict """
        self.assertIsInstance(
            self.sample_food_orders.get(1),
            dict,
            msg="Method does not return Dict"
        )
    
    def test_get_handles_out_of_range_orderid(self):
        """ Test that out of range orderid return custom error message
            (Out of range)
        """
        self.assertDictEqual(
            self.sample_food_orders.get(1),
            {"Order fetching error message": "orderid out of range"},
            msg="Method does not handle out of range orders"
        )

        self.assertDictEqual(
            self.sample_food_orders.get(-1),
            {"Order fetching error message": "orderid out of range"},
            msg="Method does not handle out of range orders"
        )

        self.assertDictEqual(
            self.sample_food_orders.get(0),
            {"Order fetching error message": "orderid out of range"},
            msg="Method does not handle out of range orders"
        )

        self.assertDictEqual(
            self.sample_food_orders.get(2),
            {"Order fetching error message": "orderid out of range"},
            msg="Method does not handle out of range orders"
        )

    def test_get_with_non_int_orderid(self):
        """ Test that invalid (non-int) orderid returns custom error message
            (only positive int)
        """
        self.assertDictEqual(
            self.sample_food_orders.get('2.0'),
            {"Order fetching error message": "orderid should be integer"},
            msg="Method does not handle non-integers for orderid"
        )

        self.assertDictEqual(
            self.sample_food_orders.get('one'),
            {"Order fetching error message": "orderid should be integer"},
            msg="Method does not handle non-integers for orderid"
        )
    

    def test_put_returns_dict(self):
        """ Test that put(orderid, order_status) returns dict """
        test_data = FoodOrders.post(self.sample_order_request_info)

        self.assertIsInstance(
            self.sample_food_orders.put(1, True),
            dict,
            msg='Method does not return a dict'
        )

    def test_put_returns_operational_message(self):
        """ Success or failure """
        self.assertIn(
            "Order status message",
            self.sample_food_orders.put(1, True),
            msg="Order status message not found"
        )

    def test_put_handles_out_of_range_orderid(self):
        """ Test that out of range orderid return custom error message
            (Out of range)
        """
        self.assertDictEqual(
            self.sample_food_orders.put(2, True),
            {"Order update error message": "orderid out of range"},
            msg="Method does not handle out of range orders"
        )

        self.assertDictEqual(
            self.sample_food_orders.put(0, True),
            {"Order update error message": "orderid out of range"},
            msg="Method does not handle out of range orders"
        )

        self.assertDictEqual(
            self.sample_food_orders.put(-1, True),
            {"Order update error message": "orderid out of range"},
            msg="Method does not handle out of range orders"
        )

    def test_put_handles_invalid_input(self):
        """ Test that invalid (non-int) orderid and or  update_status (non-bool)
            returns custom error message
        """
        self.assertDictEqual(
            self.sample_food_orders.put('2.0', True),
            {"Order update error message": "Invalid Input"},
            msg="Method does not handle non-integers for orderid"
        )

        self.assertDictEqual(
            self.sample_food_orders.put(1, "True"),
            {"Order update error message": "Invalid Input"},
            msg="Method does not handle non-integers for orderid"
        )



if __name__ == '__main__':
    unittest.main()
