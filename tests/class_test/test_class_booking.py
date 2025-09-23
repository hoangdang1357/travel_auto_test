import unittest
import sqlite3
import os
from .booking import Booking


class TestBookingClass(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        script = os.path.join(os.path.dirname(__file__), '..', '..', 'database.sql')
        with open(script, 'r', encoding='utf-8') as f:
            self.conn.executescript(f.read())
        self.conn.commit()
        # create a customer and service for bookings
        cur = self.conn.cursor()
        cur.execute('INSERT INTO customers (full_name, email, password_hash) VALUES (?, ?, ?)', ('User1', 'u1@example.com', 'h'))
        self.customer_id = cur.lastrowid
        cur.execute('INSERT INTO travel_services (price, rating, destination, flight, hotel, tour, max_travelers, title, description, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (100.0, 4.0, 'City', '', '', '', 10, 'Service1', '', '2025-10-01', '2025-10-05'))
        self.service_id = cur.lastrowid
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_create_booking(self):
        b = Booking(customer_id=self.customer_id, service_id=self.service_id, travel_date='2025-10-02', num_travelers=2, total_amount=200.0)
        bid = b.create(self.conn)
        self.assertIsNotNone(bid)
        loaded = Booking.get_by_id(self.conn, bid)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.num_travelers, 2)

    def test_update_booking(self):
        b = Booking(customer_id=self.customer_id, service_id=self.service_id, travel_date='2025-10-02', num_travelers=2, total_amount=200.0)
        bid = b.create(self.conn)
        self.assertTrue(b.update(self.conn, num_travelers=3, total_amount=300.0))
        updated = Booking.get_by_id(self.conn, bid)
        self.assertEqual(updated.num_travelers, 3)
        self.assertAlmostEqual(updated.total_amount, 300.0)

    def test_cancel_booking(self):
        b = Booking(customer_id=self.customer_id, service_id=self.service_id, travel_date='2025-10-03', num_travelers=1, total_amount=100.0)
        bid = b.create(self.conn)
        self.assertTrue(b.cancel(self.conn))
        canceled = Booking.get_by_id(self.conn, bid)
        self.assertEqual(canceled.status, 'canceled')


if __name__ == '__main__':
    unittest.main()
