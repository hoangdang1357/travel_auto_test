
import unittest
import os
import sys

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
        if os.path.exists('test.db'):
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
