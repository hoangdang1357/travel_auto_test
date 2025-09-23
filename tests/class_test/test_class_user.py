from .class_user import User
import unittest


class TestUser(unittest.TestCase):
    def test_user_stub(self):
        user = User(full_name="Test User", email="test@example.com", password_hash="hashed", phone="1234567890", address="123 Test St")
        self.assertTrue(user.register())
        user.verified = 1
        self.assertTrue(user.login("correct_password"))
        self.assertTrue(user.update_profile(full_name="Updated Name", phone="0987654321"))

    def test_register_sets_id_and_token(self):
        user = User(full_name="Reg User", email="reg@example.com", password_hash="h")
        self.assertTrue(user.register())
        # Stub sets a customer_id and verification token
        self.assertIsNotNone(user.customer_id)
        self.assertEqual(user.verified, 0)
        self.assertTrue(hasattr(user, 'verification_code'))
        self.assertEqual(user.verification_code, 'stub_token')

    def test_login_fails_before_verification(self):
        user = User(email="noverify@example.com", password_hash="h")
        user.register()
        # Not verified yet, so even correct password should fail
        self.assertFalse(user.login("correct_password"))

    def test_login_fails_with_wrong_password(self):
        user = User(email="wrongpass@example.com", password_hash="h")
        user.register()
        user.verified = 1
        # Wrong password should fail
        self.assertFalse(user.login("wrong_password"))

    def test_update_profile_partial(self):
        user = User(email="update@example.com")
        user.register()
        # Update only phone
        self.assertTrue(user.update_profile(phone="555-0000"))
        self.assertEqual(user.phone, "555-0000")
        # Update address only
        self.assertTrue(user.update_profile(address="42 New St"))
        self.assertEqual(user.address, "42 New St")
        # Update full name
        self.assertTrue(user.update_profile(full_name="New Name"))
        self.assertEqual(user.full_name, "New Name")