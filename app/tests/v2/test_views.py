""" Test cases for views.py """

import unittest
import json
from app import app


class TestHomePage(unittest.TestCase):
    """ Test Routes """
    def setUp(self):
        """ Instantiate test client """
        self.app = app.test_client()

    def test_index_status_code(self):
        """Test for home page data"""
        test_resp = self.app.get(
            '/api/v2/',
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(test_resp.status_code, 200)
        self.assertNotEqual(test_resp.status_code, 404)

    def test_index_output_data(self):
        """Test for home page status code 200(ok)"""
        test_resp = self.app.get(
            '/api/v2/',
            headers={'content-type': 'application/json'}
        )

        self.assertIn(b"Welcome User", test_resp.data, msg="Homepage message")

    

class TestSignUpRoute(unittest.TestCase):
    """ Test route to register new user """
    def setUp(self):
        """ Instantiate test client with data """
        pass
    
    def tearDown(self):
        pass
    
    def test_payload_before_posting(self):
        """ Test that function checks that data from model conforms with
            requirements before deploying the payload
        """
        pass

    def test_post_orders_status_code(self):
        """ Test that valid path and data for successful order creation
            returns HTTP status 201 and a custom message to indicate success
        """
        pass
    


    
