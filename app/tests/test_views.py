""" Test cases for views.py """

import unittest
import json
from app import app

class TestHomePage(unittest.TestCase):
    """ Test Routes """
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


        self.assertIn(b'Order placement message', test_resp.data)

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
