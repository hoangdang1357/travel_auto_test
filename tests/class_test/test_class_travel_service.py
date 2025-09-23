import unittest
import sqlite3
import os
from .travel_service import TravelService


class TestTravelServiceClass(unittest.TestCase):
    def setUp(self):
        # In-memory DB
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        script = os.path.join(os.path.dirname(__file__), '..', '..', 'database.sql')
        with open(script, 'r', encoding='utf-8') as f:
            self.conn.executescript(f.read())
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_add_edit_delete_service(self):
        svc = TravelService(title='Sample Service', price=120.5, max_travelers=10, start_date='2025-10-01', end_date='2025-10-05')
        # Add
        added = svc.save(self.conn)
        self.assertTrue(added)
        self.assertIsNotNone(svc.service_id)

        # Edit
        svc.title = 'Edited Service'
        svc.price = 200.0
        svc.max_travelers = 8
        updated = svc.save(self.conn)
        self.assertTrue(updated)
        cur = self.conn.cursor()
        cur.execute('SELECT title, price, max_travelers FROM travel_services WHERE service_id = ?', (svc.service_id,))
        row = cur.fetchone()
        self.assertEqual(row['title'], 'Edited Service')
        self.assertAlmostEqual(row['price'], 200.0)
        self.assertEqual(row['max_travelers'], 8)

        # Delete
        deleted = svc.delete(self.conn)
        self.assertTrue(deleted)
        cur.execute('SELECT * FROM travel_services WHERE service_id = ?', (svc.service_id,))
        self.assertIsNone(cur.fetchone())

    def test_availability_check(self):
        svc = TravelService(title='Limited', price=100, max_travelers=5, start_date='2025-10-10', end_date='2025-10-20')
        svc.save(self.conn)
        cur = self.conn.cursor()
        # create customers and bookings
        cur.execute('INSERT INTO customers (full_name, email, password_hash) VALUES (?, ?, ?)', ('A', 'a@example.com', 'h'))
        c1 = cur.lastrowid
        cur.execute('INSERT INTO customers (full_name, email, password_hash) VALUES (?, ?, ?)', ('B', 'b@example.com', 'h'))
        c2 = cur.lastrowid
        travel_date = '2025-10-15'
        cur.execute("INSERT INTO bookings (customer_id, service_id, booking_date, travel_date, num_travelers, status, total_amount) VALUES (?, ?, datetime('now'), ?, ?, ?, ?)",
                    (c1, svc.service_id, travel_date, 3, 'confirmed', 300.0))
        cur.execute("INSERT INTO bookings (customer_id, service_id, booking_date, travel_date, num_travelers, status, total_amount) VALUES (?, ?, datetime('now'), ?, ?, ?, ?)",
                    (c2, svc.service_id, travel_date, 2, 'confirmed', 200.0))
        self.conn.commit()

        remaining = svc.remaining_capacity(self.conn, travel_date)
        self.assertEqual(remaining, 0)

        # cancel one booking
        cur.execute("UPDATE bookings SET status = 'canceled' WHERE customer_id = ?", (c2,))
        self.conn.commit()
        remaining_after = svc.remaining_capacity(self.conn, travel_date)
        self.assertEqual(remaining_after, 2)


if __name__ == '__main__':
    unittest.main()
