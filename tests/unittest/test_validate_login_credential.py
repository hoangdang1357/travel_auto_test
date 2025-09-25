import os
import sys
import pytest
import csv

# Ensure project root on sys.path so 'auth' can be imported when running pytest
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    
from auth.routes import validate_login_credentials

def load_test_data_from_csv(filepath):
    test_cases = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            test_cases.append((
                row["email"],
                row["password"],
                row["expected_valid"] == 'True',
                row["expected_message"]
            ))
    return test_cases

@pytest.mark.parametrize("email, password, expected_valid, expected_message", load_test_data_from_csv("tests\\unittest\\csv_unit_testing\\validate_login_credential_data.csv"))
def test_validate_login_credentials(email, password, expected_valid, expected_message):
    is_valid, message = validate_login_credentials(email, password)
    assert is_valid == expected_valid
    assert message == expected_message