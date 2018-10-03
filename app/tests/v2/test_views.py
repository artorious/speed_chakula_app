""" Test cases for views.py """

import unittest
import json
from app import create_app
from app.api.v2.models import DatabaseManager

class BaseTestCase(unittest.TestCase):
    """ Base Tests """
    def setUp(self):
        self.app = create_app(config_mode='testing')
        self.app = self.app.test_client()
        self.sample_reg_info = {
            'username': 'shelockholmes',
            'email': 'consultingdetective@email.com',
            'password': 'theelephantman',
            'name': 'Arthur Ngondo'
        }
        self.sample_reg_info_bad_email = {
            'username': 'mrnoname',
            'email': 'mrnoname#@email.com',
            'password': 'elephantman',
            'name': 'Arthur Ngondo'
        }

        self.sample_reg_info_bad_password = {
            'username': 'mrnoname',
            'email': 'mrnoname@email.com',
            'password': 'passwd',
            'name': 'Arthur Ngondo'
        }
        self.test_database = DatabaseManager(config_mode='testing')
        self.test_database.create_all_tables()

        self.sample_login_info_registered = {
            'username': 'shelockholmes',
            'password': 'theelephantman'
        }

        self.sample_login_info_non_registered = {
            'username': 'ihaveneverregistered',
            'password': 'neverevernever'
        }
        #TODO: Helper methods (login/out)

    def tearDown(self):
        self.test_database.drop_all_tables()
        self.test_database.close_database()

class TestHomePage(BaseTestCase):
    """ Test Routes """


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

    

class TestAuthRoutes(BaseTestCase):
    """ Test route to register new user """
         
    def test_user_signup_status_code(self):
        """ Test that valid path and data for successful user creation
            returns HTTP status 201 
        """
        test_resp = self.app.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.sample_reg_info),
            headers={'content-type': 'application/json'}
        )     
        self.assertEqual(test_resp.status_code, 201)
        self.assertNotEqual(test_resp.status_code, 405)
        self.assertNotEqual(test_resp.status_code, 404)
        self.assertNotEqual(test_resp.status_code, 400)
    
    def test_user_signup_operational_message(self):
        """ Test that valid path and data for successful user creation
            returns a custom message to indicate success a valid auth token and content type
        """
        test_resp = self.app.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.sample_reg_info),
            headers={'content-type': 'application/json'}
        )
        resp_data = json.loads(test_resp.resp_data.decode())
        self.assertTrue(resp_data["Status"] == "Success")
        self.assertTrue(resp_data["Message"] == "Registration successful")
        self.assertTrue(resp_data["Authentication token"])
        self.assertTrue(test_resp.content_type == 'application/json')

    def test_user_signup_of_an_existing_user(self):
        """ Test that valid path and data for repeated user registration
            returns a custom message to indicate failure
        """
        self.app.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.sample_reg_info),
            headers={'content-type': 'application/json'}
        )

        test_resp = self.app.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.sample_reg_info),
            headers={'content-type': 'application/json'}
        )
        resp_data = json.loads(test_resp.resp_data.decode())
        self.assertTrue(resp_data["Status"] == "Username Error")
        self.assertTrue(resp_data["Message"] == "Username already exists. Try a different username")
        self.assertTrue(test_resp.content_type == 'application/json')
        self.assertEqual(test_resp.status_code, 202)

    def test_user_signup_with_invalid_email(self):
        """ Test that valid path and and invalid email. 
            returns a custom message to indicate failure
        """

        test_resp = self.app.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.sample_reg_info_bad_email),
            headers={'content-type': 'application/json'}
        )
        resp_data = json.loads(test_resp.resp_data.decode())
        self.assertTrue(resp_data["Status"] == "Email Error")
        self.assertTrue(resp_data["Message"] == "Invalid Email address. Check syntax and try again")
        self.assertTrue(test_resp.content_type == 'application/json')
        self.assertEqual(test_resp.status_code, 202)

    def test_user_signup_with_invalid_password(self):
        """ Test that valid path and and invalid password. 
            returns a custom message to indicate failure
        """

        test_resp = self.app.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.sample_reg_info_bad_email),
            headers={'content-type': 'application/json'}
        )
        resp_data = json.loads(test_resp.resp_data.decode())
        self.assertTrue(resp_data["Status"] == "Password Error")
        self.assertTrue(resp_data["Message"] == "Invalid password. Should be atlest 8 characters long")
        self.assertTrue(test_resp.content_type == 'application/json')
        self.assertEqual(test_resp.status_code, 202)
    
    def test_payload_before_posting_for_malformed_input(self):
        """ Test that function checks that data from model conforms with
            requirements (dict) before deploying the payload
        """
        test_resp = self.app.post(
            '/api/v2/auth/signup',
            data=json.dumps('I want to register'),
            headers={'content-type': 'application/json'}
        )
        resp_data = json.loads(test_resp.resp_data.decode())
        self.assertTrue(resp_data["Status"] == "Operation failed")
        self.assertTrue(resp_data["Message"] == "Sorry.... the provided data is malformed")
        self.assertTrue(test_resp.content_type == 'application/json')

    def test_login_of_registered_user(self):
        """ Test that a registered user can login """
        # register a user
        test_registration = self.app.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.sample_reg_info),
            headers={'content-type': 'application/json'}
        )
        resp_data = json.loads(test_resp.resp_data.decode())
        self.assertTrue(resp_data["Status"] == "Success")
        self.assertTrue(resp_data["Message"] == "Registration successful")
        self.assertTrue(resp_data["Authentication token"])
        self.assertTrue(test_resp.content_type == 'application/json')

        # Try to login
        test_resp = self.app.post(
            '/api/v2/auth/login',
            data=json.dumps(self.sample_login_info_registered),
            headers={'content-type': 'application/json'}
        )
        resp_data = json.loads(test_resp.resp_data.decode())
        self.assertEqual(resp_data.status_code, 200)
        self.assertTrue(resp_data["Status"] == "Success")
        self.assertTrue(resp_data["Message"] == "Login successful")
        self.assertTrue(resp_data["Authentication token"])
        self.assertTrue(test_resp.content_type == 'application/json')

    def test_login_of_non_registered_user(self):
        """ Test that a non-registered user cannot login """
        test_resp = self.app.post(
            '/api/v2/auth/login',
            data=json.dumps(self.sample_login_info_non_registered),
            headers={'content-type': 'application/json'}
        )
        resp_data = json.loads(test_resp.resp_data.decode())
        self.assertEqual(resp_data.status_code, 404)
        self.assertTrue(resp_data["Status"] == "Login Error")
        self.assertTrue(resp_data["Message"] == "Invalid username/password. Try again")
        self.assertTrue(test_resp.content_type == 'application/json')

    def test_login_with_malformed_input(self):
        """ Test that a malformed input cannot login """
        test_resp = self.app.post(
            '/api/v2/auth/login',
            data=json.dumps('Can I log in?'),
            headers={'content-type': 'application/json'}
        )
        resp_data = json.loads(test_resp.resp_data.decode())
        self.assertEqual(resp_data.status_code, 404)
        self.assertTrue(resp_data["Status"] == "Operation failed")
        self.assertTrue(resp_data["Message"] == "Sorry.... the provided data is malformed")
        self.assertTrue(test_resp.content_type == 'application/json')

class MenuRoutes(BaseTestCase):
    """ Tests for menu operations """

    def test_menu_fetching(self):
        """ Test that route can fetch all menu items """
        test_resp = self.app.get('/api/v2/menu')
        self.assertEqual(resp_data.status_code, 200)
        self.assertNotEqual(resp_data.status_code, 404)
        self.assertTrue(test_resp.content_type == 'application/json')
