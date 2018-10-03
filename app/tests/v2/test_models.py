""" Test cases for models.py """

import unittest
import bcrypt
from app.api.v2.models import DatabaseManager, MenuOps, OperationsOnNewUsers, UserLogs


class BaseTestCase(unittest.TestCase):
    """ Base Tests """
    def setUp(self):
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

        self.sample_login_info_registered = {
            'username': 'shelockholmes',
            'password': 'theelephantman'
        }

        self.sample_login_info_non_registered = {
            'username': 'ihaveneverregistered',
            'password': 'neverevernever'
        }

        self.test_database = DatabaseManager(config_mode='testing')
        self.test_database.create_all_tables()
        self.sample_user = OperationsOnNewUsers(self.sample_reg_info)
        self.sample_user2 = OperationsOnNewUsers(self.sample_reg_info_bad_email)
        self.sample_user3 = OperationsOnNewUsers(self.sample_reg_info_bad_password)
        self.menu_instance = MenuOps()
    
    def tearDown(self):
        self.test_database.drop_all_tables()
        self.test_database.close_database()
        


class TestOperationsOnNewUsers(BaseTestCase):
    """ Test user registration """

    def test_username_check(self):
        """ Test that a username does not exist before registration"""
        self.assertIn(
            "Username Error",
            self.sample_user2,
            msg="Taken Username"
        )
    
    def test_password_check(self):
        self.assertIn(
            "Invalid Password",
            self.sample_user3.password_check(),
            msg="Invalid password"
        )
    
    def test_email_check(self):
        self.assertIn(
            "Invalid Email",
            self.sample_user2.email_check(),
            msg="Invalid email provided"
        )
    

    def test_register_operation_success(self):
        registration_msg = self.sample_user.register_user()
        self.assertIn(
            "Registration success",
            registration_msg,
            msg="User account not created succesfully"
        )
    
    def test_fetch_menu_items_returns_dict(self):
        """ Test that menu items in databse_returns dict """
        test_dict = self.menu_instance.fetch_menu_items()
        self.assertIsInstance(test_dict, dict, msg="method does not return dictionry")

class TestUserLogs(BaseTestCase):
    """ Tests cases for logged in/out users """
    def test_login_operation_registered_user(self):
        """ Test that a registered user can login """
        # Register a user
        registration_msg = self.sample_user.register_user()
        self.assertIn(
            "Registration success",
            registration_msg,
            msg="User account not created succesfully"
        )

        # login with
        legit_login_details = self.sample_login_info_registered
        test_legit_login = UserLogs(legit_login_details)
        
        invalid_login_details = self.sample_login_info_non_registered
        test_invalid_login = UserLogs(invalid_login_details)

        valid_login = test_legit_login.fetch_and_verify_user_login()
        invalid_login = test_invalid_login.fetch_and_verify_user_login()
        
        self.assertTrue(valid_login)
        self.assertFalse(invalid_login)
