""" Test cases for models.py """

import unittest
import bcrypt
from app.api.v2.models import DatabaseManager, UserOps


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
        self.test_database = DatabaseManager(config_mode='testing')
        self.test_database.create_all_tables()
        self.sample_user = UserOps(self.sample_reg_info)
        self.sample_user2 = UserOps(self.sample_reg_info_bad_email)
        self.sample_user3 = UserOps(self.sample_reg_info_bad_password)

    def tearDown(self):
        self.test_database.drop_all_tables()
        self.test_database.close_database()

class TestUserOps(BaseTestCase):
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
            "Password Error",
            self.sample_user2,
            msg="Invalid password"
        )
    
    def test_email_check(self):
        self.assertIn(
            "Email Error",
            self.sample_user2.email_check(),
            msg="Invalid email"
        )
    
    def test_gen_passwd_hash(self):
        tester = bcrypt.hashpw('theelephantman', bcrypt.gensalt())
        self.assertEqual(
            tester, 
            self.sample_user.hashed_password,
            msg="verify password hashing"
        )

    
    def test_post_operation_success(self):
        self.assertIn(
            "Success",
            self.sample_user,
            msg="User account not created succesfully"
        )
    
    def test_auth_token_encoding(self):
        auth_token = self.sample_user.auth_token_encoding(self.sample_user.verified_username)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_auth_token_decoding(self):
        auth_token = self.sample_user.auth_token_encoding(self.sample_user.verified_username)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(
            self.sample_user.auth_token_decoding(auth_token) == self.sample_user.encoded_token
        )
