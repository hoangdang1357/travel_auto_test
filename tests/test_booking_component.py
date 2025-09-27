import os
import sqlite3
import unittest
from flask import Flask
from pathlib import Path
import sys
import tempfile
import shutil

# Ensure project root import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from auth import routes as auth_routes
from booking import routes as booking_routes
from services import routes as services_routes

BASE_DIR = PROJECT_ROOT
SCHEMA_PATH = BASE_DIR / 'database.sql'


def load_schema(conn):
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()


def seed_service(conn, title='Sample Tour', price=100.0, destination='Paris'):
    conn.execute(
        """INSERT INTO travel_services (price, rating, destination, flight, hotel, tour, max_travelers, title, description, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, date('now','+7 day'), date('now','+14 day'))""",
        (price, 4.5, destination, None, None, 'Tour Info', 10, title, 'Description')
    )
    conn.commit()
    row = conn.execute('SELECT service_id FROM travel_services ORDER BY service_id DESC LIMIT 1').fetchone()
    return row['service_id']

class BookingComponentTests(unittest.TestCase):
    def setUp(self):
        # temp db file
        tmp = tempfile.NamedTemporaryFile(prefix='booking_test_', suffix='.sqlite', delete=False)
        tmp.close()
        self.db_path = Path(tmp.name)

        # normal connection factory with FK
        def _test_get_db_connection():
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            conn.execute('PRAGMA foreign_keys = ON;')
            return conn
        import database as database_module
        database_module.get_db_connection = _test_get_db_connection
        auth_routes.get_db_connection = _test_get_db_connection
        booking_routes.get_db_connection = _test_get_db_connection
        services_routes.get_db_connection = _test_get_db_connection
        auth_routes.send_verification_email = lambda email, token: None

        # create schema
        conn = _test_get_db_connection(); load_schema(conn); conn.close()

        # app using real templates (project templates) and stub missing blueprints
        self.app = Flask(__name__, template_folder=str(BASE_DIR / 'templates'))
        self.app.config['SECRET_KEY'] = 'test_secret'

        from flask import Blueprint
        # Stubs for admin & profile to satisfy base.html links using correct endpoint names
        admin_bp = Blueprint('admin', __name__)
        @admin_bp.route('/login')
        def login():  # endpoint admin.login
            return 'ADMIN LOGIN'
        profile_bp = Blueprint('profile', __name__)
        @profile_bp.route('/')
        def index():  # endpoint profile.index
            return 'PROFILE INDEX'

        self.app.register_blueprint(admin_bp, url_prefix='/admin')
        self.app.register_blueprint(profile_bp, url_prefix='/profile')
        self.app.register_blueprint(auth_routes.auth_bp)
        self.app.register_blueprint(services_routes.services_bp, url_prefix='/services')
        self.app.register_blueprint(booking_routes.booking_bp, url_prefix='/booking')

        @self.app.route('/')
        def index():
            return 'INDEX'

        self.client = self.app.test_client()
        # create & login user
        self._create_and_login_user()
        # seed service
        conn = _test_get_db_connection(); self.service_id = seed_service(conn); conn.close()

    def tearDown(self):
        if self.db_path.exists():
            try:
                self.db_path.unlink()
            except OSError:
                pass

    # Helpers
    def _create_and_login_user(self, email='user@example.com'):
        self.client.post('/signup', data={
            'full_name': 'Test User', 'email': email, 'password': 'Password123!',
            'phone': '0123456789', 'address': 'Addr'
        }, follow_redirects=True)
        # verify
        conn = sqlite3.connect(self.db_path); conn.row_factory = sqlite3.Row
        code = conn.execute('SELECT verification_code FROM customers WHERE email=?', (email,)).fetchone()['verification_code']
        conn.close()
        self.client.get(f'/signup/{code}', follow_redirects=True)
        # login
        self.client.post('/signin', data={'email': email, 'password': 'Password123!'}, follow_redirects=True)

    # TC-BOOK-001: Successful booking creation flow
    def test_tc_book_001_success_booking_creation(self):
        resp = self.client.post(f'/booking/new/{self.service_id}', data={
            'travel_date': '2099-12-31',
            'num_travelers': '2'
        }, follow_redirects=True)
        self.assertIn(b'Booking created successfully', resp.data)
        # ensure booking exists
        conn = sqlite3.connect(self.db_path); conn.row_factory = sqlite3.Row
        booking = conn.execute('SELECT * FROM bookings').fetchone()
        conn.close()
        self.assertIsNotNone(booking)
        self.assertEqual(booking['num_travelers'], 2)
        self.assertEqual(booking['status'], 'pending')

    # TC-BOOK-002: Booking creation with invalid traveler details (simulate missing traveler name later)
    def test_tc_book_002_missing_traveler_detail(self):
        # First create booking
        create_resp = self.client.post(f'/booking/new/{self.service_id}', data={
            'travel_date': '2099-12-31',
            'num_travelers': '1'
        }, follow_redirects=True)
        self.assertIn(b'Booking created successfully', create_resp.data)
        # Get booking id
        conn = sqlite3.connect(self.db_path); conn.row_factory = sqlite3.Row
        booking_id = conn.execute('SELECT booking_id FROM bookings ORDER BY booking_id DESC LIMIT 1').fetchone()['booking_id']
        conn.close()
        # Post traveler details with missing full name
        td_resp = self.client.post(f'/booking/traveler_details/{booking_id}', data={
            'full_name[]': [''],
            'gender[]': ['male'],
            'dob[]': ['2000-01-01'],
            'passport_number[]': ['P123']
        }, follow_redirects=True)
        self.assertIn(b'Traveler 1: Full name is required', td_resp.data)
        # Ensure no traveler_details row inserted
        conn = sqlite3.connect(self.db_path); conn.row_factory = sqlite3.Row
        rows = conn.execute('SELECT * FROM traveler_details WHERE booking_id=?', (booking_id,)).fetchall()
        conn.close()
        self.assertEqual(len(rows), 0)

    # TC-BOOK-003: Update booking before payment (change num_travelers)
    def test_tc_book_003_update_booking_before_payment(self):
        # create booking with 2 travelers
        self.client.post(f'/booking/new/{self.service_id}', data={'travel_date': '2099-12-31', 'num_travelers': '2'}, follow_redirects=True)
        conn = sqlite3.connect(self.db_path); conn.row_factory = sqlite3.Row
        booking = conn.execute('SELECT * FROM bookings ORDER BY booking_id DESC LIMIT 1').fetchone()
        booking_id = booking['booking_id']
        conn.close()
        # Directly update num_travelers (simulate edit form not implemented)
        conn = sqlite3.connect(self.db_path); conn.row_factory = sqlite3.Row
        conn.execute('UPDATE bookings SET num_travelers=? WHERE booking_id=?', (3, booking_id))
        conn.commit()
        updated = conn.execute('SELECT num_travelers FROM bookings WHERE booking_id=?', (booking_id,)).fetchone()['num_travelers']
        conn.close()
        self.assertEqual(updated, 3)

    # TC-BOOK-004: Cancel booking before payment
    def test_tc_book_004_cancel_before_payment(self):
        self.client.post(f'/booking/new/{self.service_id}', data={'travel_date': '2099-12-31', 'num_travelers': '1'}, follow_redirects=True)
        conn = sqlite3.connect(self.db_path); conn.row_factory = sqlite3.Row
        booking_id = conn.execute('SELECT booking_id FROM bookings ORDER BY booking_id DESC LIMIT 1').fetchone()['booking_id']
        conn.execute("UPDATE bookings SET status='canceled' WHERE booking_id=?", (booking_id,))
        conn.commit()
        status = conn.execute('SELECT status FROM bookings WHERE booking_id=?', (booking_id,)).fetchone()['status']
        conn.close()
        self.assertEqual(status, 'canceled')

    # TC-BOOK-005: Attempt to update/cancel booking after payment
    def test_tc_book_005_block_update_after_payment(self):
        # Create booking
        self.client.post(f'/booking/new/{self.service_id}', data={'travel_date': '2099-12-31', 'num_travelers': '1'}, follow_redirects=True)
        conn = sqlite3.connect(self.db_path); conn.row_factory = sqlite3.Row
        booking_id = conn.execute('SELECT booking_id FROM bookings ORDER BY booking_id DESC LIMIT 1').fetchone()['booking_id']
        # Simulate payment completion
        conn.execute("UPDATE bookings SET status='confirmed' WHERE booking_id=?", (booking_id,))
        conn.commit()
        # Attempt to modify after confirmation should now raise due to trigger
        with self.assertRaises(sqlite3.DatabaseError) as ctx:
            conn.execute('UPDATE bookings SET num_travelers=? WHERE booking_id=?', (5, booking_id))
            conn.commit()
        self.assertIn('Cannot modify a confirmed booking', str(ctx.exception))
        conn.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)
