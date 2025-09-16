
import unittest
import os
import sys

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from database import init_db, get_db_connection
from werkzeug.security import generate_password_hash

class AdminTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DATABASE'] = 'test.db'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            init_db()
            # Add a sample admin user
            conn = get_db_connection()
            password_hash = generate_password_hash('adminpassword')
            conn.execute('INSERT INTO admins (username, password_hash, email) VALUES (?, ?, ?)',
                         ('admin', password_hash, 'admin@example.com'))
            conn.commit()
            conn.close()
        self.admin_login()

    def tearDown(self):
        os.remove('test.db')

    def admin_login(self):
        self.app.post('/admin/login', data=dict(
            username='admin',
            password='adminpassword'
        ), follow_redirects=True)

    def test_add_service(self):
        with self.app as c:
            response = c.post('/admin/add_service', data=dict(
                title='New Service',
                description='A new service description',
                destination='New Destination',
                price=500,
                rating=4.5,
                start_date='2026-01-01',
                end_date='2026-01-10',
                max_travelers=10,
                flight='Flight details',
                hotel='Hotel details',
                tour='Tour details'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Service added successfully!', response.data)

            # Verify the service in the database
            with app.app_context():
                conn = get_db_connection()
                service = conn.execute('SELECT * FROM travel_services WHERE title = ?', ('New Service',)).fetchone()
                conn.close()
                self.assertIsNotNone(service)
                self.assertEqual(service['destination'], 'New Destination')

    def test_edit_service(self):
        with self.app as c:
            # First, add a service to edit
            c.post('/admin/add_service', data=dict(
                title='Service to Edit',
                description='A service to be edited',
                destination='Original Destination',
                price=600,
                rating=4.0,
                start_date='2026-02-01',
                end_date='2026-02-10',
                max_travelers=5,
                flight='Flight details',
                hotel='Hotel details',
                tour='Tour details'
            ), follow_redirects=True)

            # Get the service_id
            with app.app_context():
                conn = get_db_connection()
                service = conn.execute('SELECT * FROM travel_services WHERE title = ?', ('Service to Edit',)).fetchone()
                service_id = service['service_id']
                conn.close()

            # Now, edit the service
            response = c.post(f'/admin/edit_service/{service_id}', data=dict(
                title='Edited Service',
                description='An edited service description',
                destination='Edited Destination',
                price=700,
                rating=4.8,
                start_date='2026-03-01',
                end_date='2026-03-10',
                max_travelers=8,
                flight='Edited flight details',
                hotel='Edited hotel details',
                tour='Edited tour details'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Service updated successfully!', response.data)

            # Verify the changes in the database
            with app.app_context():
                conn = get_db_connection()
                edited_service = conn.execute('SELECT * FROM travel_services WHERE service_id = ?', (service_id,)).fetchone()
                conn.close()
                self.assertEqual(edited_service['title'], 'Edited Service')
                self.assertEqual(edited_service['destination'], 'Edited Destination')

    def test_delete_service(self):
        with self.app as c:
            # First, add a service to delete
            c.post('/admin/add_service', data=dict(
                title='Service to Delete',
                description='A service to be deleted',
                destination='Delete Destination',
                price=800,
                rating=3.0,
                start_date='2026-04-01',
                end_date='2026-04-10',
                max_travelers=3,
                flight='Flight details',
                hotel='Hotel details',
                tour='Tour details'
            ), follow_redirects=True)

            # Get the service_id
            with app.app_context():
                conn = get_db_connection()
                service = conn.execute('SELECT * FROM travel_services WHERE title = ?', ('Service to Delete',)).fetchone()
                service_id = service['service_id']
                conn.close()

            # Now, delete the service
            response = c.post(f'/admin/delete_service/{service_id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Service deleted successfully!', response.data)

            # Verify the service is deleted from the database
            with app.app_context():
                conn = get_db_connection()
                deleted_service = conn.execute('SELECT * FROM travel_services WHERE service_id = ?', (service_id,)).fetchone()
                conn.close()
                self.assertIsNone(deleted_service)

    def signup_and_login(self):
        self.app.post('/auth/signup', data=dict(
            full_name='Test Customer',
            email='customer@example.com',
            password='password',
            phone='1234567890',
            address='123 Customer St'
        ), follow_redirects=True)
        self.app.post('/auth/signin', data=dict(
            email='customer@example.com',
            password='password'
        ), follow_redirects=True)

    def test_service_availability(self):
        """This test exposes a bug where the application does not check for service availability."""
        with self.app as c:
            # First, add a service with max_travelers = 1
            c.post('/admin/add_service', data=dict(
                title='Limited Service',
                description='A service with limited availability',
                destination='Limited Destination',
                price=100,
                rating=5.0,
                start_date='2026-05-01',
                end_date='2026-05-10',
                max_travelers=1,
                flight='Flight details',
                hotel='Hotel details',
                tour='Tour details'
            ), follow_redirects=True)

            # Get the service_id
            with app.app_context():
                conn = get_db_connection()
                service = conn.execute('SELECT * FROM travel_services WHERE title = ?', ('Limited Service',)).fetchone()
                service_id = service['service_id']
                conn.close()

            # Sign up and log in a customer
            self.signup_and_login()

            # Try to book the service for 2 travelers (should fail, but it will pass due to a bug)
            response = c.post(f'/booking/new/{service_id}', data=dict(
                travel_date='2026-05-05',
                num_travelers=2
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Booking created successfully! Please provide traveler details.', response.data)

if __name__ == '__main__':
    unittest.main()
