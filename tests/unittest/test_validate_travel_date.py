import os
import sys
import pytest

# Ensure project root on sys.path so 'app' and local packages can be imported when pytest's CWD varies
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from booking.routes import validate_travel_date
import datetime
import csv
def load_test_data_from_csv(filepath):
    test_cases = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            test_cases.append((
                row["input_date"],
                row["expected_valid"] == 'True',
                row["expected_message"]
            ))
    return test_cases

@pytest.mark.parametrize("input_date, expected_valid, expected_message", load_test_data_from_csv("tests\\unittest\\csv_unit_testing\\validate_travel_date.csv"))
def test_validate_travel_date(input_date, expected_valid, expected_message):
    is_valid, message = validate_travel_date(input_date)
    assert is_valid == expected_valid
    assert message == expected_message