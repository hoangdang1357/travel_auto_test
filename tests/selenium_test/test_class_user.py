from class_user import User
import unittest
import time

class TestUser(unittest.TestCase):
    def test_user_stub(self):
        user = User(full_name="Test User", email="test@example.com", password_hash="hashed", phone="1234567890", address="123 Test St")
        self.assertTrue(user.register())
        user.verified = 1
        self.assertTrue(user.login("correct_password"))
        self.assertTrue(user.update_profile(full_name="Updated Name", phone="0987654321"))