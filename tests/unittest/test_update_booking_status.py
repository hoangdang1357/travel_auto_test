import os
import sys
import pytest
from unittest.mock import MagicMock, patch
import csv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from admin.routes import update_booking_status_in_db

def load_data_from_csv(filepath):
    test_cases = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            test_cases.append((
                int(row["booking_id"]),
                row["status"],
                row["expected_result"] == 'True'
            ))
    return test_cases

@pytest.mark.parametrize("booking_id, status, expected_result", load_data_from_csv("tests\\unittest\\csv_unit_testing\\update_booking_status_data.csv"))
def test_update_booking_status_in_db(booking_id, status, expected_result):
    bookings = {
        1: {"status": "pending"},
        2: {"status": "confirmed"},
    }

    with patch("admin.routes.get_db_connection") as mock_conn:
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        def fake_execute(query, params):
            # Simulate DB execute: set cursor.rowcount to 1 when booking exists
            if params[1] in bookings:
                bookings[params[1]]["status"] = params[0]
                mock_cursor.rowcount = 1
                return True
            mock_cursor.rowcount = 0
            return False

        # admin.routes uses cursor.execute(...), so attach side_effect to mock_cursor.execute
        mock_cursor.execute.side_effect = fake_execute
        mock_connection.commit.return_value = None

        result = update_booking_status_in_db(booking_id, status)
        assert result == expected_result

        if expected_result:
            assert bookings[booking_id]["status"] == status