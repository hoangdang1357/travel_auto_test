import os
import sys
import tempfile
import sqlite3
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app
import database
import booking.routes as booking_routes
import admin.routes as admin_routes


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
        self._orig_routes_get = booking_routes.get_db_connection
        self._orig_admin_get = admin_routes.get_db_connection

        def _get_conn():
            c = sqlite3.connect(self.db_path)
            c.row_factory = sqlite3.Row
            return c

        database.get_db_connection = _get_conn
        booking_routes.get_db_connection = _get_conn
        admin_routes.get_db_connection = _get_conn
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        database.get_db_connection = self._orig_get
        booking_routes.get_db_connection = self._orig_routes_get
        admin_routes.get_db_connection = self._orig_admin_get
        self.tmpdir.cleanup()


@pytest.fixture()
def client():
    with TempDB():
        app.config.update(TESTING=True)
        with app.test_client() as client:
            yield client


def seed_admin_user():
    # username: admin, password: admin
    from werkzeug.security import generate_password_hash
    conn = database.get_db_connection()
    conn.execute(
        """
        INSERT INTO admins (username, password_hash, email)
        VALUES (?, ?, ?)
        """,
        (
            'admin',
            generate_password_hash('admin'),
            'admin@example.com',
        ),
    )
    conn.commit()
    conn.close()


def seed_customer_and_service_and_booking():
    conn = database.get_db_connection()
    # customer
    cur = conn.execute(
        """
        INSERT INTO customers (full_name, email, password_hash, phone, address, verified)
        VALUES (?, ?, ?, ?, ?, 1)
        """,
        (
            'Test User',
            'test@example.com',
            'hash',
            '0123456789',
            'Hanoi',
        ),
    )
    customer_id = cur.lastrowid
    # service
    cur = conn.execute(
        """
        INSERT INTO travel_services (price, rating, destination, flight, hotel, tour, max_travelers, title, description, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            100.0,
            4.0,
            'Tokyo, Japan',
            'Flight',
            'Hotel',
            'Tour',
            10,
            'A trip to Tokyo',
            'Desc',
            '2025-12-01',
            '2025-12-08',
        ),
    )
    service_id = cur.lastrowid
    # booking (pending)
    cur = conn.execute(
        """
        INSERT INTO bookings (customer_id, service_id, travel_date, num_travelers, total_amount)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            customer_id,
            service_id,
            '2025-12-02',
            1,
            100.0,
        ),
    )
    booking_id = cur.lastrowid
    conn.commit()
    conn.close()
    return booking_id


def test_admin_can_update_booking_status(client):
    seed_admin_user()
    booking_id = seed_customer_and_service_and_booking()

    # Admin login
    resp = client.post(
        "/admin/login",
        data={"username": "admin", "password": "admin"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Logged in successfully" in resp.data

    # View bookings page
    resp = client.get("/admin/bookings")
    assert resp.status_code == 200
    assert str(booking_id).encode() in resp.data

    # Update status to 'canceled'
    resp = client.post(
        f"/admin/update_booking_status/{booking_id}",
        data={"status": "canceled"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Booking status updated successfully" in resp.data

    # Verify in DB
    conn = database.get_db_connection()
    row = conn.execute("SELECT status FROM bookings WHERE booking_id = ?", (booking_id,)).fetchone()
    conn.close()
    assert row is not None
    assert row[0] == 'canceled'


def test_admin_confirms_booking_reflected_in_history(client):
    seed_admin_user()
    booking_id = seed_customer_and_service_and_booking()

    # Admin login
    resp = client.post(
        "/admin/login",
        data={"username": "admin", "password": "admin"},
        follow_redirects=True,
    )
    assert resp.status_code == 200

    # Update status to 'confirmed'
    resp = client.post(
        f"/admin/update_booking_status/{booking_id}",
        data={"status": "confirmed"},
        follow_redirects=True,
    )
    assert resp.status_code == 200

    # Simulate customer session and load history
    # Get the customer_id for this booking
    conn = database.get_db_connection()
    row = conn.execute("SELECT customer_id FROM bookings WHERE booking_id = ?", (booking_id,)).fetchone()
    customer_id = row[0]
    conn.close()

    with client.session_transaction() as sess:
        sess['customer_id'] = customer_id

    resp = client.get("/booking/history")
    assert resp.status_code == 200
    # Confirmed should appear in the history table
    assert b"confirmed" in resp.data
