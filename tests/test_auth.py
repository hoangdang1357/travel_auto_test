<<<<<<< HEAD
import unittest
import os
import sys
from auth.routes import signup, signin
=======

import unittest
import os
import sys
>>>>>>> 1f58bd4957a6ed3a7d95c8be6cb16bb83b883c07

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

<<<<<<< HEAD
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
=======
from app import app
from database import init_db, get_db_connection

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DATABASE'] = 'test.db'
        self.app = app.test_client()
        with app.app_context():
            init_db()

    def tearDown(self):
        os.remove('test.db')

    def test_signup(self):
        response = self.app.post('/auth/signup', data=dict(
            full_name='Test User',
            email='test@example.com',
            password='password',
            phone='1234567890',
            address='123 Test St'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created successfully! Please sign in.', response.data)

    def test_signin(self):
        # First, sign up a user
        self.app.post('/auth/signup', data=dict(
            full_name='Test User',
            email='test@example.com',
            password='password',
            phone='1234567890',
            address='123 Test St'
        ), follow_redirects=True)

        # Now, sign in
        response = self.app.post('/auth/signin', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Signed in successfully!', response.data)

    def test_invalid_signin(self):
        response = self.app.post('/auth/signin', data=dict(
            email='wrong@example.com',
            password='wrongpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email or password.', response.data)

if __name__ == '__main__':
    unittest.main()
>>>>>>> 1f58bd4957a6ed3a7d95c8be6cb16bb83b883c07
