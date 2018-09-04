""" Test cases for views.py """

from app import app
import unittest


class TestRoutesCases(unittest.TestCase):
    """ Test Routes """

    def setUp(self):
        """ Instantiate test client """
        self.app = app.test_client()
    
    def test_fetch_all_orders_operation_success(self):
        """ Test that a valid path that returns HTTP response code of 200(OK)
        """
        test_resp = self.app.get(
            '/api/v1/orders',
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(
            test_resp.status_code, 200, msg='Expected 200'
        )


    def test_fetch_all_orders_operation_malformed_route(self):
        """ Test that a path with an error (malformed syntax) returns an 
            appropriate error message in JSON and HTTP response code of 
            404 (NOT FOUND)
        """
        test_resp = self.app.get(
            '/api/v1/orderss',
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(
            test_resp.status_code,
            404,
            msg='Error: The requested URL was not found on the server'
        )
