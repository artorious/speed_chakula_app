""" Test cases for models.py """

from app.models import FoodOrders
import unittest


class TestFoodOrders(unittest.TestCase):
    """ Test FoodOrders class """

    def setUp(self):
        """ Instantiate """
        self.sample_food_orders = FoodOrders()
     
    def test_class_inits_with_dict(self):
        """ Test class inits with a dict """
        self.assertIsInstance(
            self.sample_food_orders.all_food_orders, dict,
            msg='Class does not initialize with a dict'
        )
    
    def test_fetch_all_food_orders_return_value(self):
        """ Test that fetch_all_food_orders() returns a dictionary """
        self.assertIsInstance(
            self.sample_food_orders.fetch_all_food_orders(), dict,
            msg='Method should return a dict'
        )
