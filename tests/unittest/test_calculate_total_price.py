import os
import sys
import pytest

# Ensure project root on sys.path so 'booking' can be imported when running pytest
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from booking.routes import calculate_total_amount
import csv
def load_test_data_from_csv(filepath):
    test_cases = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            test_cases.append((
                float(row["price"]),
                int(row["num_travelers"]),
                float(row.get("tax", 0.0)),
                float(row.get("discount", 0.0)),
                float(row["expected"]),
            ))
    return test_cases

@pytest.mark.parametrize("price, num_travelers, tax, discount, expected", load_test_data_from_csv("tests\\unittest\\csv_unit_testing\\calculate_total_price.csv"))
def test_calculate_total_amount(price, num_travelers, tax, discount, expected):
    result = calculate_total_amount(price, num_travelers, tax, discount)
    assert result == expected