import unittest
import os
import sys
from auth.routes import signup, signin

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestAuth(unittest.TestCase):
    def test_signup_success(self):
        success, msg = signup({"email": "test@example.com", "password": "123"})
        self.assertTrue(success)
        self.assertIn("ok", msg)

    def test_signup_duplicate(self):
        signup({"email": "dup@example.com", "password": "111"})
        success, msg = signup({"email": "dup@example.com", "password": "111"})
        self.assertFalse(success)
        self.assertIn("failed", msg)

    def test_signup_missing_email(self):
        success, msg = signup({"password": "noemail"})
        self.assertFalse(success)

    def test_signin_success(self):
        signup({"email": "login@example.com", "password": "abc"})
        success, msg = signin({"email": "login@example.com", "password": "abc"})
        self.assertTrue(success)
        self.assertIn("ok", msg)

    def test_signin_wrong_password(self):
        signup({"email": "wrong@example.com", "password": "good"})
        success, msg = signin({"email": "wrong@example.com", "password": "bad"})
        self.assertFalse(success)

    def test_signin_not_registered(self):
        success, msg = signin({"email": "ghost@example.com", "password": "xxx"})
        self.assertFalse(success)
