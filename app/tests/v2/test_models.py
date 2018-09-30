""" Test cases for models.py """

import unittest
import bcrypt
from app.api.v2.models import DatabaseManager, UserOps


class TestUserOps(unittest.TestCase):
    """ Test user registration """
    def setUp(self):
        """ Define test vars """
        # self.app = create_app(config_mode="development")
        test_db = DatabaseManager(config_mode='testing')
        
        self.sample_reg_info = {
            'username': 'mrnoname',
            'email': 'mrnoname@email.com',
            'password': 'elephantman',
            'name': 'Arthur Ngondo',
        }

        self.sample_reg_info_bad_email = {
            'username': 'mrnoname',
            'email': 'mrnoname#@email.com',
            'password': 'elephantman',
            'name': 'Arthur Ngondo',
        }

        self.sample_reg_info_bad_password = {
            'username': 'mrnoname',
            'email': 'mrnoname@email.com',
            'password': 'passwd',
            'name': 'Arthur Ngondo',
        }
        
        self.sample_user = UserOps(self.sample_reg_info)
        self.sample_user2 = UserOps(self.sample_reg_info_bad_email)
        self.sample_user3 = UserOps(self.sample_reg_info_bad_password)

    def tearDown(self):
        pass
    
    def test_username_check(self):
        """ Test that a username does not exist before registration"""
        sample_user2 = UserOps(self.sample_reg_info)
        self.assertIn(
            "Username Error",
            sample_user2,
            msg="Taken Username"
        )
    
    def test_password_check(self):
        sample_user2 = UserOps(self.sample_reg_info_bad_password)
        self.assertIn(
            "Password Error",
            sample_user2,
            msg="Invalid password"
        )
    
    def test_email_check(self):
        
        self.assertIn(
            "Email Error",
            self.sample_user2.email_check(),
            msg="Invalid email"
        )
    
    def test_gen_passwd_hash(self):
        tester = bcrypt.hashpw('elephantman', bcrypt.gensalt())
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
