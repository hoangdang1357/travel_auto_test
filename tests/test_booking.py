
import unittest
import os
import sys

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from database import init_db, add_sample_data

class BookingTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DATABASE'] = 'test.db'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            init_db()
            add_sample_data()
        self.signup_and_login()

    def tearDown(self):
        os.remove('test.db')

    def signup_and_login(self):
        self.app.post('/auth/signup', data=dict(
            full_name='Test User',
            email='test@example.com',
            password='password',
            phone='1234567890',
            address='123 Test St'
        ), follow_redirects=True)
        self.app.post('/auth/signin', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)

    def test_new_booking(self):
        with self.app as c:
            # The login happens in setUp
            response = c.post('/booking/new/1', data=dict(
                travel_date='2025-12-25',
                num_travelers=2
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Traveler Details', response.data)

    def test_booking_history(self):
        with self.app as c:
            # First, create a booking
            c.post('/booking/new/1', data=dict(
                travel_date='2025-12-25',
                num_travelers=2
            ), follow_redirects=True)
            # Now, check the history
            response = c.get('/booking/history', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'My Bookings', response.data)
            self.assertIn(b'A trip to Paris', response.data)

if __name__ == '__main__':
    unittest.main()
