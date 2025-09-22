import unittest
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions import validate_login_credentials


class TestAuthValidation(unittest.TestCase):
    def test_valid_credentials(self):
        valid, msg = validate_login_credentials("user@example.com", "securepass")
        self.assertTrue(valid)
        self.assertEqual(msg, "")

    def test_missing_email(self):
        valid, msg = validate_login_credentials("", "password123")
        self.assertFalse(valid)
        self.assertIn("required", msg)

    def test_invalid_email_format(self):
        valid, msg = validate_login_credentials("invalidemail", "password123")
        self.assertFalse(valid)
        self.assertIn("Invalid email format", msg)

    def test_short_password(self):
        valid, msg = validate_login_credentials("user@example.com", "123")
        self.assertFalse(valid)
        self.assertIn("at least 6 characters", msg)

    def test_missing_password(self):
        valid, msg = validate_login_credentials("user@example.com", "")
        self.assertFalse(valid)
        self.assertIn("required", msg)
