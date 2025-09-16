
import unittest
import os
import sys
from booking.routes import calculate_total_amount
# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestBookingCalculation(unittest.TestCase):
    def test_single_traveler(self):
        price = 100.0
        num_travelers = 1
        total = calculate_total_amount(price, num_travelers)
        self.assertEqual(total, 100.0)

    def test_multiple_travelers(self):
        price = 200.0
        num_travelers = 3
        total = calculate_total_amount(price, num_travelers)
        self.assertEqual(total, 600.0)
        
    def test_negative_travelers(self):
        price = 50.0
        num_travelers = -2
        total = calculate_total_amount(price, num_travelers)
        self.assertEqual(total, -100.0)

    def test_zero_travelers(self):
        price = 150.0
        num_travelers = 0
        total = calculate_total_amount(price, num_travelers)
        self.assertEqual(total, 0.0)
        
    def test_decimal_travelers(self):
        price = 75
        num_travelers = 2.5
        total = calculate_total_amount(price, num_travelers)
        # expect error
        with self.assertRaises(TypeError):
            calculate_total_amount(price, num_travelers)

    def test_negative_price(self):
        price = -50.0
        num_travelers = 2
        total = calculate_total_amount(price, num_travelers)
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

