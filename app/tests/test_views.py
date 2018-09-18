""" Test cases for views.py """

import unittest
import json
from app import app

class TestHomePage(unittest.TestCase):
    def setUp(self):
        pass

    def test_index_status_code(self):
        # is 200
        # also No 404
        pass

    def test_index_output_data(self):
        pass

    def tearDown(self):
        pass

class TestOrdersRoutes(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_get_orders_status_code(self):
        # is 200
        # also No 404
        pass
    
    def test_post_orders_status_code(self):
        # is 201
        # Not 405
        # Not 404
        # Not 400
        pass

    def test_payload_to_place_a_new_order(self):
        """ Test that function checks that data from model conforms with
            requirements before deploying the payload
        """
        pass

    def tearDown(self):
        pass

class TestOrderByIdRoutes(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_order_by_id_status_code(self):
        # is 200
        # also No 404
        pass
    
    def test_get_order_by_id_response_data(self):
        # make one and see
        pass
    
    def test_put_order_by_id_status_code(self):
        # is 200
        # not 404
        pass
    
    def test_put_order_by_id_response_data(self):
        # Success message
        pass
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
