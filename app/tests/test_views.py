""" Test cases for views.py """

import unittest
import json
from app import app


class TestRoutesCases(unittest.TestCase):
    """ Test Routes """

    def setUp(self):
        """ Instantiate test client """
        self.app = app.test_client()
        self.sample_order_request_info = {
            'username': 'mrnoname',
            'user_tel': '0727161173',
            'order_qty': 2,
            'order_description': '500ml soda @Ksh. 100/=',
            'user_location': '221B Baker st.'
        }

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

    def test_place_new_order_operation_successs(self):
        """ Test that valid path and data for successful order creation
            returns HTTP status 201 and a custom message to indicate success
        """
        test_resp = self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order_request_info),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(test_resp.status_code, 200)
        self.assertIn(b'Order placement message', test_resp.data)

    def test_place_new_order_operation_malformed_route(self):
        """ Test that path with an error (malformed syntax) returns an
            appropriate error message in JSON and HTTP response code of
            404 (BAD REQUEST)
        """
        test_resp = self.app.post(
            '/api/v1/orderss',
            data=json.dumps(self.sample_order_request_info),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(
            404,
            test_resp.status_code,
            msg='Resource NOT Found. Order NOT created'
        )

    def test_payload_to_place_a_new_order(self):
        """ Test that function checks that data from model conforms with
            requirements before deploying the payload
        """
        test_resp = self.app.post(
            '/api/v1/orders',
            data=json.dumps('I want everthing'),
            headers={'content-type': 'application/json'}
        )
        self.assertIn(b'Sorry.... Order placement Failed', test_resp.data)

    def test_fetch_one_order_operation_success(self):
        """ Test that a  non-error path returns a single order in JSON and 
            HTTP response code of 200 (OK)
        """
        self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order_request_info),
            headers={'content-type': 'application/json'}
        )

        test_resp = test_resp = self.app.get(
            '/api/v1/orders/1',
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(
            test_resp.status_code, 200, msg='Expected 200'
        )

    def test_fetch_one_order_operation_with_malformed_route(self):
        """ Test that a path with an error(non-existent) returns an appropriate
            error message in JSON and HTTP response code of 404(NOT FOUND)
        """
        self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order_request_info),
            headers={'content-type': 'application/json'}
        )

        test_resp = self.app.get(
            '/api/v1/orderss/1',
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(
            test_resp.status_code,
            404,
            msg='Error: The requested URL was not found on the server'
        )

    def test_fetch_one_order_operation_with_invalid_orderid(self):
        """ Test that invalid orderId returns custom error message 
            (only positive int)
        """
        self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order_request_info),
            headers={'content-type': 'application/json'}
        )

        test_resp = test_resp = self.app.get(
            '/api/v1/orders/one',
            headers={'content-type': 'application/json'}
        )
        
        self.assertIn(
            b"Order fetching error message",
            test_resp,
            msg="Route does not handle non-integers for orderID"
        )

    def test_fetch_one_order_operation_with_out_of_range_orderid(self):
        """ Test that out of range orderId returns custom error message 
            (Out of range) - 416 Requested Range Not Satisfiable
        """
        self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order_request_info),
            headers={'content-type': 'application/json'}
        )

        test_resp = test_resp = self.app.get(
            '/api/v1/orders/2',
            headers={'content-type': 'application/json'}
        )
        
        self.assertIn(
            b"Order fetching error message",
            test_resp,
            msg="Route does not handle out of range integers for orderID"
        )

        test_resp = test_resp = self.app.get(
            '/api/v1/orders/0',
            headers={'content-type': 'application/json'}
        )
        self.assertIn(
            b"Order fetching error message",
            test_resp,
            msg="Route does not handle out of range integers for orderID"
        )

if __name__ == '__main__':
    unittest.main()
