""" Test cases for models.py """

import unittest
import bcrypt
from app.api.v2.models import SignUp


class TestSignUp(unittest.TestCase):
    """ Test user registration """
    def setUp(self):
        """ Define test vars """

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
        
        self.sample_user = SignUp(self.sample_reg_info)

    def tearDown(self):
        pass
    
    def test_username_check(self):
        self.assertIn(
            "Username Error",
            SignUp(self.sample_reg_info),
            msg="Taken Username"
        )
    
    def test_password_check(self):
        self.assertIn(
            "Password Error",
            SignUp(self.sample_reg_info_bad_password),
            msg="Invalid password"
        )
    
    def test_email_check(self):
        self.assertIn(
            "Email Error",
            SignUp(self.sample_reg_info_bad_email),
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
        sample_user = SignUp(self.sample_reg_info)
        auth_token = sample_user.auth_token_encoding(sample_user.verified_username)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_auth_token_decoding(self):
        sample_user = SignUp(self.sample_reg_info)
        auth_token = sample_user.auth_token_encoding(
            sample_user.verified_username
        )
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(
            sample_user.auth_token_decoding(auth_token) == 'mrnoname'
        )
