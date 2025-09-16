
import unittest
import os
import sys

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from database import init_db, get_db_connection

class AuthTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        # Use an absolute path for the test database
        cls.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test.db')
        app.config['DATABASE'] = cls.db_path
        
        # Ensure the database is clean before the first test
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
        
        with app.app_context():
            init_db()

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.db_path)
        except FileNotFoundError:
            pass

    def setUp(self):
        self.app = app.test_client()
        # Clean the database before each test
        with app.app_context():
            conn = get_db_connection()
            conn.execute("DELETE FROM customers")
            conn.commit()


    def test_signup(self):
        response = self.app.post('/auth/signup', data=dict(
            full_name='Signup User',
            email='signup@example.com',
            password='password',
            phone='1234567890',
            address='123 Signup St'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created successfully! Please check your email to verify your account.', response.data)

    def test_signin(self):
        # First, sign up a user
        self.app.post('/auth/signup', data=dict(
            full_name='Test User',
            email='test@example.com',
            password='password',
            phone='1234567890',
            address='123 Test St'
        ), follow_redirects=True)

        # Manually verify the user for testing purposes
        with app.app_context():
            conn = get_db_connection()
            conn.execute("UPDATE customers SET verified = 1 WHERE email = 'test@example.com'")
            conn.commit()
            conn.close()

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

    def test_edit_profile(self):
        # First, sign up and sign in a user
        self.app.post('/auth/signup', data=dict(
            full_name='Test User',
            email='test@example.com',
            password='password',
            phone='1234567890',
            address='123 Test St'
        ), follow_redirects=True)
        
        # Manually verify the user for testing purposes
        with app.app_context():
            conn = get_db_connection()
            conn.execute("UPDATE customers SET verified = 1 WHERE email = 'test@example.com'")
            conn.commit()
            conn.close()
            
        self.app.post('/auth/signin', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)

        # Now, edit the profile
        response = self.app.post('/profile/edit', data=dict(
            full_name='New Name',
            phone='0987654321',
            address='456 New St'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile updated successfully!', response.data)

        # Verify the changes in the database
        with app.app_context():
            conn = get_db_connection()
            customer = conn.execute('SELECT * FROM customers WHERE email = ?', ('test@example.com',)).fetchone()
            conn.close()
            self.assertEqual(customer['full_name'], 'New Name')
            self.assertEqual(customer['phone'], '0987654321')
            self.assertEqual(customer['address'], '456 New St')

if __name__ == '__main__':
    unittest.main()
