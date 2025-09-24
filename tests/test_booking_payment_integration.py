import os
import sys
import tempfile
import sqlite3
import datetime
import pytest
from flask import session

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app
import database
import booking.routes as booking_routes

SCHEMA_SQL = None


def load_schema_sql():
    global SCHEMA_SQL
    if SCHEMA_SQL is None:
        schema_path = os.path.join(PROJECT_ROOT, 'database.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            SCHEMA_SQL = f.read()
    return SCHEMA_SQL


class TempDB:
    def __init__(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmpdir.name, 'test.db')

    def __enter__(self):
        # Initialize a fresh DB from schema
        conn = sqlite3.connect(self.db_path)
        conn.executescript(load_schema_sql())
        conn.commit()
        conn.close()
        # Monkeypatch database.get_db_connection to point to this DB
        self._orig_get = database.get_db_connection
        self._orig_routes_get = booking_routes.get_db_connection

        def _get_conn():
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn

        database.get_db_connection = _get_conn
        booking_routes.get_db_connection = _get_conn
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        database.get_db_connection = self._orig_get
        booking_routes.get_db_connection = self._orig_routes_get
        self.tmpdir.cleanup()


@pytest.fixture()
def client():
    # Use a temp DB per test
    with TempDB():
        app.config.update(TESTING=True)
        with app.test_client() as client:
            yield client


def seed_user_and_service():
    conn = database.get_db_connection()
    # Seed a verified customer
    conn.execute(
        """
        INSERT INTO customers (full_name, email, password_hash, phone, address, verified)
        VALUES (?, ?, ?, ?, ?, 1)
        """,
        (
            'Test User',
            'test@example.com',
            'pbkdf2:sha256:260000$oYlPwT9zC2qF5N6H$756066f8a3a9427c2f2b505c0d384e8e6a9a6a1d6d3d3b5b7a4b693c1fd7a9a0',
            # Not used by signin route in integration path, could be any hash
            '0123456789',
            'Hanoi',
        ),
    )
    # Seed a travel service
    cur = conn.execute(
        """
        INSERT INTO travel_services (price, rating, destination, flight, hotel, tour, max_travelers, title, description, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            199.99,
            4.5,
            'Tokyo, Japan',
            'Flight A380',
            'Hotel Tokyo',
            'Shibuya Crossing Tour',
            10,
            'A trip to Tokyo',
            'Experience Tokyo',
            '2025-12-01',
            '2025-12-08',
        ),
    )
    service_id = cur.lastrowid
    conn.commit()
    conn.close()
    return service_id


def login_session(client, customer_id):
    # Set session customer_id to simulate login
    with client.session_transaction() as sess:
        sess['customer_id'] = customer_id


def get_customer_id_by_email(email):
    conn = database.get_db_connection()
    row = conn.execute('SELECT customer_id FROM customers WHERE email = ?', (email,)).fetchone()
    conn.close()
    return row['customer_id']


def test_booking_to_payment_flow(client):
    service_id = seed_user_and_service()
    customer_id = get_customer_id_by_email('test@example.com')
    login_session(client, customer_id)

    # 1) Create new booking (POST /booking/new/<service_id>)
    resp = client.post(
        f"/booking/new/{service_id}",
        data={
            'travel_date': '2025-12-02',
            'num_travelers': '2',
        },
        follow_redirects=False,
    )
    assert resp.status_code in (302, 303)
    # Should redirect to traveler_details
    assert '/booking/traveler_details/' in resp.headers['Location']

    # Extract booking_id from redirect URL
    booking_id = int(resp.headers['Location'].rstrip('/').split('/')[-1])

    # 2) Submit traveler details (POST /booking/traveler_details/<id>)
    traveler_payload = {
        'full_name[]': ['Alice Example', 'Bob Example'],
        'gender[]': ['female', 'male'],
        'dob[]': ['1995-01-01', '1990-02-02'],
        'passport_number[]': ['P1234567', 'P7654321'],
    }
    resp = client.post(
        f"/booking/traveler_details/{booking_id}",
        data=traveler_payload,
        follow_redirects=False,
    )
    assert resp.status_code in (302, 303)
    assert f"/booking/payment/{booking_id}" in resp.headers['Location']

    # 3) Make payment (POST /booking/payment/<id>)
    resp = client.post(
        f"/booking/payment/{booking_id}",
        data={'payment_method': 'credit_card'},
        follow_redirects=False,
    )
    assert resp.status_code in (302, 303)
    assert "/booking/history" in resp.headers['Location']

    # 4) Verify DB updates: booking status confirmed, payment row exists
    conn = database.get_db_connection()
    booking = conn.execute('SELECT status, total_amount FROM bookings WHERE booking_id = ?', (booking_id,)).fetchone()
    payment = conn.execute('SELECT payment_method, amount, status FROM payments WHERE booking_id = ?', (booking_id,)).fetchone()
    conn.close()

    assert booking is not None
    assert booking['status'] == 'confirmed'
    assert payment is not None
    assert payment['payment_method'] == 'credit_card'
    # total_amount price(199.99) * travelers(2)
    assert float(payment['amount']) == pytest.approx(199.99 * 2, rel=1e-3)
    assert payment['status'] == 'paid'


def test_booking_validation_errors(client):
    """Past travel_date and invalid num_travelers should fail with proper messages."""
    service_id = seed_user_and_service()
    customer_id = get_customer_id_by_email('test@example.com')
    login_session(client, customer_id)

    # 1) Past date should fail
    past_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    resp = client.post(
        f"/booking/new/{service_id}",
        data={'travel_date': past_date, 'num_travelers': '1'},
        follow_redirects=True,
    )
    # Should render the same form with a flash message; ensure no redirect to traveler_details
    assert resp.status_code == 200
    assert b"Travel date cannot be in the past" in resp.data
    assert b"/booking/traveler_details/" not in resp.data

    # 2) Invalid travelers count (0) should fail
    valid_future = (datetime.date.today() + datetime.timedelta(days=10)).strftime('%Y-%m-%d')
    resp = client.post(
        f"/booking/new/{service_id}",
        data={'travel_date': valid_future, 'num_travelers': '0'},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Number of travelers must be a positive integer" in resp.data
    # No booking should be created; verify DB has zero bookings
    conn = database.get_db_connection()
    cnt = conn.execute('SELECT COUNT(*) AS c FROM bookings').fetchone()['c']
    conn.close()
    assert cnt == 0


def test_booking_invalid_date_format(client):
    """Malformed date format should trigger the invalid format message and not create bookings."""
    service_id = seed_user_and_service()
    customer_id = get_customer_id_by_email('test@example.com')
    login_session(client, customer_id)

    # Provide a malformed date '31/12/2025' (DD/MM/YYYY) which is not in accepted formats
    resp = client.post(
        f"/booking/new/{service_id}",
        data={'travel_date': '31/12/2025', 'num_travelers': '1'},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    # Message text from validate_travel_date
    assert b"Invalid date format. Use YYYY-MM-DD" in resp.data
    # Ensure no booking rows inserted
    conn = database.get_db_connection()
    cnt = conn.execute('SELECT COUNT(*) AS c FROM bookings').fetchone()['c']
    conn.close()
    assert cnt == 0
