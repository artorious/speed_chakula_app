""" Test cases for models.py """

from app.models import FoodOrders
import unittest


class TestFoodOrders(unittest.TestCase):
    """ Test FoodOrders class """

    def setUp(self):
        pass
     
    def test_class_inits_with_dict(self):
        """ Test class inits with an empty dict """
        pass

    def test_fetch_all_food_orders_returns_dict(self):
        """ Test method returns appropriate nested dict with sample data """
        pass
    
    def test_fetch_all_orders_operation_without_orders(self):
        """ Test method returns of a custom  messege when no orders have
            been placed (empty orders dict)
        """
        pass
