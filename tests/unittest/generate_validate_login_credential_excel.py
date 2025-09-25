import csv
from pathlib import Path
from openpyxl import Workbook
import sys

# Ensure project root on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from auth.routes import validate_login_credentials
from unittest.mock import patch, MagicMock


CSV_PATH = Path(__file__).parent / 'csv_unit_testing' / 'validate_login_credential_data.csv'
OUTPUT_XLSX = Path(__file__).parent / 'validate_login_credential_summary.xlsx'


def load_csv(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def run_case(email, password):
    # Recreate the same mocks used in the test file
    users = {
        "hoangdang1368@gmail.com": {
            "email": "hoangdang1368@gmail.com",
            "password_hash": "fakehash",
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

    def fake_check(hash_value, pwd):
        return email == "hoangdang1368@gmail.com" and pwd == "Hoang123123"

    with patch('auth.routes.get_db_connection') as mock_conn, patch('auth.routes.check_password_hash') as mock_check:
        mock_connection = MagicMock()
        mock_conn.return_value = mock_connection
        mock_connection.execute.return_value.fetchone = fake_fetchone
        mock_check.side_effect = fake_check

        result = validate_login_credentials(email, password)

    return result


def make_workbook(rows):
    wb = Workbook()
    ws = wb.active
    ws.title = 'validate_login_credential'

    headers = ['Test case ID', 'Module', 'Description', 'Prior condition', 'Input data', 'Step', 'Expected result', 'Actual result', 'Status']
    ws.append(headers)

    for i, r in enumerate(rows, start=1):
        tc_id = f"TC-{i:03d}"
        email = r.get('email')
        password = r.get('password')
        expected_valid = r.get('expected_valid') == 'True'
        expected_message = r.get('expected_message')

        description = f"validate_login_credentials(email={email})"
        prior = 'N/A'
        input_data = f"email={email}, password={'*' * len(password or '')}"
        step = 'Call validate_login_credentials with DB/password mocks'
        expected_result = f"{expected_valid} => '{expected_message}'"

        actual_valid, actual_message = run_case(email, password)
        actual_result = f"{actual_valid} => '{actual_message}'"
        status = 'Pass' if (actual_valid == expected_valid and actual_message == expected_message) else 'Fail'

        ws.append([tc_id, 'auth.routes', description, prior, input_data, step, expected_result, actual_result, status])

    return wb


def main():
    if not CSV_PATH.exists():
        print(f"CSV not found at {CSV_PATH}")
        return 2

    rows = load_csv(CSV_PATH)
    wb = make_workbook(rows)
    wb.save(OUTPUT_XLSX)
    print(f"Wrote Excel summary to {OUTPUT_XLSX}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
