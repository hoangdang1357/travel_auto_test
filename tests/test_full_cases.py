import unittest
from utils.validation import (
    calculate_total_amount,
    validate_travel_dates,
    validate_login,
    update_booking_status
)

class TestFullCases(unittest.TestCase):

    # --- calculate_total_amount ---
    def test_tc001_valid_single_traveler(self):
        self.assertEqual(calculate_total_amount(100, 1, tax=0, discount=0), 100.00)

    def test_tc002_valid_multiple_travelers(self):
        self.assertEqual(calculate_total_amount(200, 2, tax=0, discount=0), 400.00)

    def test_tc003_valid_with_tax(self):
        self.assertEqual(calculate_total_amount(200, 2, tax=0.1, discount=0), 440.00)

    def test_tc004_valid_with_discount(self):
        self.assertEqual(calculate_total_amount(150, 2, tax=0, discount=0.2), 240.00)

    def test_tc005_valid_tax_and_discount(self):
        self.assertEqual(calculate_total_amount(100, 3, tax=0.1, discount=0.1), 297.00)

    def test_tc006_negative_price(self):
        with self.assertRaises(ValueError):
            calculate_total_amount(-100, 1)

    def test_tc007_zero_travelers(self):
        with self.assertRaises(ValueError):
            calculate_total_amount(100, 0)

    def test_tc008_negative_travelers(self):
        with self.assertRaises(ValueError):
            calculate_total_amount(100, -2)

    def test_tc009_negative_discount(self):
        with self.assertRaises(ValueError):
            calculate_total_amount(100, 1, discount=-0.1)

    def test_tc010_discount_gt_one(self):
        with self.assertRaises(ValueError):
            calculate_total_amount(100, 1, discount=1.5)

    def test_tc011_negative_tax(self):
        with self.assertRaises(ValueError):
            calculate_total_amount(100, 1, tax=-0.2)

    def test_tc012_tax_gt_one(self):
        with self.assertRaises(ValueError):
            calculate_total_amount(100, 1, tax=1.2)

    def test_tc013_boundary_price_zero(self):
        with self.assertRaises(ValueError):
            calculate_total_amount(0, 1)

    # --- validate_travel_dates ---
    def test_tc014_valid_dates(self):
        self.assertTrue(validate_travel_dates("2025-10-01", "2025-10-10"))

    def test_tc015_end_before_start(self):
        self.assertFalse(validate_travel_dates("2025-10-10", "2025-10-01"))

    def test_tc016_same_day(self):
        self.assertFalse(validate_travel_dates("2025-10-01", "2025-10-01"))

    def test_tc017_missing_start(self):
        with self.assertRaises(ValueError):
            validate_travel_dates("", "2025-10-10")

    def test_tc018_missing_end(self):
        with self.assertRaises(ValueError):
            validate_travel_dates("2025-10-01", "")

    def test_tc019_wrong_format(self):
        with self.assertRaises(ValueError):
            validate_travel_dates("01-10-2025", "10-10-2025")

    # --- validate_login ---
    def test_tc020_valid_login(self):
        self.assertTrue(validate_login("admin", "1234", users_db={"admin":"1234"}))

    def test_tc021_wrong_password(self):
        self.assertFalse(validate_login("admin", "wrong", users_db={"admin":"1234"}))

    def test_tc022_empty_username(self):
        self.assertFalse(validate_login("", "1234", users_db={"admin":"1234"}))

    def test_tc023_empty_password(self):
        self.assertFalse(validate_login("admin", "", users_db={"admin":"1234"}))

    def test_tc024_both_empty(self):
        self.assertFalse(validate_login("", "", users_db={"admin":"1234"}))

    def test_tc025_username_too_long(self):
        long_username = "a" * 256
        with self.assertRaises(ValueError):
            validate_login(long_username, "1234", users_db={"admin":"1234"})

    def test_tc026_password_too_short(self):
        with self.assertRaises(ValueError):
            validate_login("admin", "12", users_db={"admin":"1234"})

    # --- update_booking_status ---
    def test_tc027_update_confirmed(self):
        bookings = {1: {"status": "pending"}}
        self.assertEqual(update_booking_status(1, "confirmed", bookings_db=bookings), "confirmed")
        self.assertEqual(bookings[1]["status"], "confirmed")

    def test_tc028_update_cancelled(self):
        bookings = {2: {"status": "pending"}}
        self.assertEqual(update_booking_status(2, "cancelled", bookings_db=bookings), "cancelled")
        self.assertEqual(bookings[2]["status"], "cancelled")

    def test_tc029_update_pending(self):
        bookings = {3: {"status": "confirmed"}}
        self.assertEqual(update_booking_status(3, "pending", bookings_db=bookings), "pending")
        self.assertEqual(bookings[3]["status"], "pending")

    def test_tc030_empty_status(self):
        with self.assertRaises(ValueError):
            update_booking_status(1, "", bookings_db={1:{"status":"pending"}})

    def test_tc031_unknown_status(self):
        with self.assertRaises(ValueError):
            update_booking_status(1, "unknown", bookings_db={1:{"status":"pending"}})

    def test_tc032_booking_id_none(self):
        with self.assertRaises(ValueError):
            update_booking_status(None, "confirmed", bookings_db={1:{"status":"pending"}})

    def test_tc033_booking_id_negative(self):
        with self.assertRaises(ValueError):
            update_booking_status(-5, "confirmed", bookings_db={1:{"status":"pending"}})


if __name__ == "__main__":
    unittest.main()
