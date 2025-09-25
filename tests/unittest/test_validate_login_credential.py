import os
import sys
import pytest
import csv
from unittest.mock import patch, MagicMock

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


@pytest.mark.parametrize(
    "email, password, expected_valid, expected_message",
    load_test_data_from_csv("tests\\unittest\\csv_unit_testing\\validate_login_credential_data.csv")
)
def test_validate_login_credentials(email, password, expected_valid, expected_message):
    # Fake user DB
    users = {
        "hoangdang1368@gmail.com": {
            "email": "hoangdang1368@gmail.com",
            "password_hash": "fakehash",  # we’ll override with mock
            "verified": 1,
            "customer_id": 1,
            "full_name": "Hoang Dang"
        },
        "khongphaihoang@example.com": {
            "email": "khongphaihoang@example.com",
            "password_hash": "fakehash",
            "verified": 0,
            "customer_id": 3,
            "full_name": "0phaihoangdau"
        }
    }

    def fake_fetchone():
        return users.get(email, None)

    with patch("auth.routes.get_db_connection") as mock_conn, \
         patch("auth.routes.check_password_hash") as mock_check:

        # Patch DB connection
        mock_connection = MagicMock()
        mock_conn.return_value = mock_connection
        mock_connection.execute.return_value.fetchone = fake_fetchone

        # Patch password check (only accept Hoang123123)
        def fake_check(hash_value, pwd):
            return email == "hoangdang1368@gmail.com" and pwd == "Hoang123123"

        mock_check.side_effect = fake_check

        # Run test
        is_valid, message = validate_login_credentials(email, password)
        assert is_valid == expected_valid
        assert message == expected_message
