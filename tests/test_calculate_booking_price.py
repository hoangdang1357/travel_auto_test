import unittest
import os, sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions import calculate_total_amount


class TestBookingCalculation(unittest.TestCase):
    def test_single_traveler(self):
        total = calculate_total_amount(100.0, 1)
        self.assertEqual(total, 100.0)

    def test_multiple_travelers(self):
        total = calculate_total_amount(200.0, 3)
        self.assertEqual(total, 600.0)

    def test_zero_travelers(self):
        total = calculate_total_amount(150.0, 0)
        self.assertEqual(total, 0.0)

    def test_negative_travelers(self):
        total = calculate_total_amount(50.0, -2)
        self.assertEqual(total, -100.0)

    def test_decimal_travelers(self):
        with self.assertRaises(TypeError):
            calculate_total_amount(75, 2.5)

    def test_negative_price(self):
        total = calculate_total_amount(-50.0, 2)
        self.assertEqual(total, -100.0)

    def test_non_numeric_inputs(self):
        with self.assertRaises(TypeError):
            calculate_total_amount("100", 2)
        with self.assertRaises(TypeError):
            calculate_total_amount(100, "2")
        with self.assertRaises(TypeError):
            calculate_total_amount(None, 2)
        with self.assertRaises(TypeError):
            calculate_total_amount(100, None)
