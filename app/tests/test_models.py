""" Test cases for models.py """

import unittest
from app.models import FoodOrders, FoodOrderOps

class TestFoodOrders(unittest.TestCase):
    """ Test FoodOrders class """
    def setUp(self):
        pass
    
    def test_get_returns_dict(self):
        """ Test that get() method returns a dictionary """
        pass
    
    def test_get_returns_msg_when_dict_is_empty(self):
        pass
    
    def test_get_returns_dict_with_correct_format_when_orders_exist(self):
        pass
    
    def test_post_only_accepts_dicts_as_input(self):
        pass

    def test_post_only_accepts_populated_dict_of_correct_format(self):
        pass

    def test_post_returns_operation_msg_to_user(self):
        pass
    
    def tearDown(self):
        pass

class TestFoodOrdersOps(unittest.TestCase):
    """ Test FoodOrdersOps class """
    
    def setUp(self):
        pass
    
    def test_get_returns_dict_of_correct_format(self):
        """ Test that get(orderid) returns dict """
        pass
    
    def test_get_handles_out_of_range_orderid(self):
        """ Test that out of range orderid return custom error message
            (Out of range)
        """
        pass

    def test_get_with_non_int_orderid(self):
        """ Test that invalid (non-int) orderid returns custom error message
            (only positive int)
        """
        pass
    
    def test_get_handles_negative_int_as_order_id(self):
        pass

    def test_put_returns_dict(self):
        """ Test that put(orderid, order_status) returns dict """
        pass

    def test_put_returns_operational_message(self):
        """ Success or failure """
        pass

    def test_put_handles_out_of_range_orderid(self):
        """ Test that out of range orderid return custom error message
            (Out of range)
        """
        pass

    def test_put_handles_invalid_input(self):
        """ Test that invalid (non-int) orderid and or  update_status (non-bool)
            returns custom error message
        """
        pass



if __name__ == '__main__':
    unittest.main()
