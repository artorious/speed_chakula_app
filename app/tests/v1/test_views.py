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
            '/api/v1/',
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(test_resp.status_code, 200)
        self.assertNotEqual(test_resp.status_code, 404)

    def test_index_output_data(self):
        """Test for home page status code 200(ok)"""
        test_resp = self.app.get(
            '/api/v1/',
            headers={'content-type': 'application/json'}
        )

        self.assertIn(b"Welcome User", test_resp.data, msg="Homepage message")

    def tearDown(self):
        pass

class TestOrdersRoutes(unittest.TestCase):
    """ Test routes """
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

    def test_get_orders_status_code(self):
        """ Test that a valid path that returns HTTP response code of 200(OK)
        """
        test_resp = self.app.get(
            '/api/v1/orders',
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(
            test_resp.status_code, 200, msg='Expected 200'
        )
        self.assertNotEqual(
            test_resp.status_code, 404, msg='Expected 200'
        )

    def test_post_orders_status_code(self):
        """ Test that valid path and data for successful order creation
            returns HTTP status 201 and a custom message to indicate success
        """
        test_resp = self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order_request_info),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(test_resp.status_code, 200)
        self.assertNotEqual(test_resp.status_code, 405)
        self.assertNotEqual(test_resp.status_code, 404)
        self.assertNotEqual(test_resp.status_code, 400)


        self.assertIn(b"Success", test_resp.data)

    def test_payload_before_posting(self):
        """ Test that function checks that data from model conforms with
            requirements before deploying the payload
        """
        test_resp = self.app.post(
            '/api/v1/orders',
            data=json.dumps('I want everthing'),
            headers={'content-type': 'application/json'}
        )
        self.assertIn(b'Sorry.... Order placement Failed', test_resp.data)

    def tearDown(self):
        pass

class TestOrderByIdRoutes(unittest.TestCase):
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

    def test_get_order_by_id_status_code(self):
        """ Test that a valid path that returns HTTP response code of 200(OK)
        """
        self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order_request_info),
            headers={'content-type': 'application/json'}
        )

        test_resp = self.app.get(
            '/api/v1/orders/1',
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(
            test_resp.status_code, 200, msg='Expected 200'
        )
        self.assertNotEqual(
            test_resp.status_code, 404, msg='Expected 200'
        )


    def test_put_order_by_id_status_code(self):
        """ Test that a  non-error path returns a single order in JSON and
            HTTP response code of 200 (OK)
        """
        self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order_request_info),
            headers={'content-type': 'application/json'}
        )

        test_resp = self.app.put(
            '/api/v1/orders/1',
            data=json.dumps(True),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(
            test_resp.status_code, 200, msg='Expected 200'
        )
        self.assertNotEqual(
            test_resp.status_code, 404, msg='Expected 200'
        )

    def test_put_order_by_id_response_data(self):
        """ Test that a  non-error path updates a single order's accept_status
            in JSON and returns a Success message
        """
        self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order_request_info),
            headers={'content-type': 'application/json'}
        )

        test_resp = self.app.put(
            '/api/v1/orders/1',
            data=json.dumps(True),
            headers={'content-type': 'application/json'}
        )

        self.assertIn(
            b"Order status message",
            test_resp.data,
            msg="Does not output success msg to user"
        )

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
