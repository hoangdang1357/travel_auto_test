import unittest
import os, sys, datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions import validate_travel_date


class TestValidateTravelDate(unittest.TestCase):
    def test_valid_future_date(self):
        future_date = (datetime.date.today() + datetime.timedelta(days=5)).strftime("%Y-%m-%d")
        valid, msg = validate_travel_date(future_date)
        self.assertTrue(valid)
        self.assertEqual(msg, "")

    def test_past_date(self):
        past_date = (datetime.date.today() - datetime.timedelta(days=5)).strftime("%Y-%m-%d")
        valid, msg = validate_travel_date(past_date)
        self.assertFalse(valid)
        self.assertIn("past", msg)

    def test_invalid_format(self):
        valid, msg = validate_travel_date("2025/09/18")
        self.assertFalse(valid)
        self.assertIn("Invalid date format", msg)

    def test_empty_string(self):
        valid, msg = validate_travel_date("")
        self.assertFalse(valid)
        self.assertIn("required", msg)

    def test_none_input(self):
        valid, msg = validate_travel_date(None)
        self.assertFalse(valid)
        self.assertIn("required", msg)

    def test_random_string(self):
        valid, msg = validate_travel_date("random text")
        self.assertFalse(valid)
        self.assertIn("Invalid date format", msg)
