import os
import sys
import tempfile
import sqlite3
import datetime
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app
import database
import booking.routes as booking_routes
import auth.routes as auth_routes
import services.routes as services_routes


def load_schema_sql():
    schema_path = os.path.join(PROJECT_ROOT, 'database.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        return f.read()


class TempDB:
    def __init__(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmpdir.name, 'test.db')

    def __enter__(self):
        conn = sqlite3.connect(self.db_path)
        conn.executescript(load_schema_sql())
        conn.commit()
        conn.close()
        self._orig_get = database.get_db_connection
        self._orig_booking_get = booking_routes.get_db_connection
        self._orig_auth_get = auth_routes.get_db_connection
        self._orig_services_get = services_routes.get_db_connection

        def _get_conn():
            c = sqlite3.connect(self.db_path)
            c.row_factory = sqlite3.Row
            return c

        database.get_db_connection = _get_conn
        booking_routes.get_db_connection = _get_conn
        auth_routes.get_db_connection = _get_conn
        services_routes.get_db_connection = _get_conn
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        database.get_db_connection = self._orig_get
        booking_routes.get_db_connection = self._orig_booking_get
        auth_routes.get_db_connection = self._orig_auth_get
        services_routes.get_db_connection = self._orig_services_get
        self.tmpdir.cleanup()


@pytest.fixture()
def client():
    with TempDB():
        app.config.update(TESTING=True)
        with app.test_client() as client:
            yield client


def seed_service():
    conn = database.get_db_connection()
    cur = conn.execute(
        """
        INSERT INTO travel_services (price, rating, destination, flight, hotel, tour, max_travelers, title, description, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            250.0,
            4.7,
            'Tokyo, Japan',
            'Flight A380',
            'Hotel Tokyo',
            'Shibuya Tour',
            20,
            'A trip to Tokyo',
            'Experience Tokyo',
            '2025-12-01',
            '2025-12-08',
        ),
    )
    sid = cur.lastrowid
    conn.commit()
    conn.close()
    return sid


def test_full_flow_register_login_search_book_pay_history(client):
    email = 'flow@example.com'
    resp = client.post(
        "/auth/signup",
        data={
            'full_name': 'Flow User',
            'email': email,
            'password': 'Secret123',
            'phone': '0123456789',
            'address': 'Hanoi',
        },
        follow_redirects=False,
    )
    assert resp.status_code in (302, 303)

    conn = database.get_db_connection()
    row = conn.execute(
        'SELECT verification_code, customer_id FROM customers WHERE email = ?', (email,)
    ).fetchone()
    conn.close()
    token = row['verification_code']
    assert token

    resp = client.get(f"/auth/signup/{token}", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Email verified successfully" in resp.data

    resp = client.post(
        "/auth/signin",
        data={'email': email, 'password': 'Secret123'},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Signed in successfully" in resp.data

    service_id = seed_service()
    resp = client.get("/services/?destination=Tokyo")
    assert resp.status_code == 200
    assert b"A trip to Tokyo" in resp.data

    future_date = (datetime.date.today() + datetime.timedelta(days=10)).strftime('%Y-%m-%d')
    resp = client.post(
        f"/booking/new/{service_id}",
        data={'travel_date': future_date, 'num_travelers': '1'},
        follow_redirects=False,
    )
    assert resp.status_code in (302, 303)
    assert '/booking/traveler_details/' in resp.headers['Location']
    booking_id = int(resp.headers['Location'].rstrip('/').split('/')[-1])

    traveler_payload = {
        'full_name[]': ['Flow User'],
        'gender[]': ['male'],
        'dob[]': ['1990-01-01'],
        'passport_number[]': ['X1234567'],
    }
    resp = client.post(
        f"/booking/traveler_details/{booking_id}",
        data=traveler_payload,
        follow_redirects=False,
    )
    assert resp.status_code in (302, 303)
    assert f"/booking/payment/{booking_id}" in resp.headers['Location']

    resp = client.post(
        f"/booking/payment/{booking_id}",
        data={'payment_method': 'credit_card'},
        follow_redirects=False,
    )
    assert resp.status_code in (302, 303)
    assert "/booking/history" in resp.headers['Location']

    resp = client.get("/booking/history")
    assert resp.status_code == 200
    assert b"A trip to Tokyo" in resp.data
    assert b"confirmed" in resp.data
