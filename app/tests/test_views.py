""" Test cases for views.py """

from app import app
import unittest


class TestRoutesCases(unittest.TestCase):
    """ Test Routes """

    def setUp(self):
        """ Instantiate test client """
        pass
    
    def test_fetch_all_orders_operation_success(self):
        """ Test that a valid path that returns HTTP response code of 200(OK)
        """
        pass


    def test_fetch_all_orders_operation_malformed_route(self):
        """ Test that a path with an error (malformed syntax) returns an 
            appropriate error message in JSON and HTTP response code of 
            400 (BAD REQUEST)
        """
        pass

    def test_fetch_all_orders_operation_non_existent_resource(self):
        """ Test that path with error(non-existent resource returns an 
            appropriate error message in JSON and HTTP response 
            code of 404(NOT FOUND)
        """
        pass

