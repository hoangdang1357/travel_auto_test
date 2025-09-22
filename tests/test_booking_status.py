import unittest
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions import update_booking_status


class TestBookingStatus(unittest.TestCase):
    def test_valid_status_update(self):
        success, msg = update_booking_status(1, "confirmed")
        self.assertTrue(success)
        self.assertIn("updated", msg)

    def test_invalid_status(self):
        success, msg = update_booking_status(1, "done")
        self.assertFalse(success)
        self.assertIn("Invalid status", msg)

    def test_invalid_booking_id(self):
        success, msg = update_booking_status(-5, "confirmed")
        self.assertFalse(success)
        self.assertIn("Invalid booking ID", msg)

    def test_non_numeric_booking_id(self):
        success, msg = update_booking_status("abc", "pending")
        self.assertFalse(success)
        self.assertIn("Invalid booking ID", msg)
