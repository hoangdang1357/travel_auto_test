import csv
import re
import tempfile
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from openpyxl import Workbook


CSV_PATH = Path(__file__).parent / 'csv_unit_testing' / 'update_booking_status_data.csv'
OUTPUT_XLSX = Path(__file__).parent / 'update_booking_status_summary.xlsx'
PYTEST_FILE = Path(__file__).parent / 'test_update_booking_status.py'


def load_csv(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def run_pytest_and_get_results(pytest_path):
    # Run pytest and produce junit xml in a temp file
    with tempfile.NamedTemporaryFile(prefix='junit-', suffix='.xml', delete=False) as tmp:
        junit_path = Path(tmp.name)

    cmd = [
        str(Path(sys.executable)), '-m', 'pytest', str(pytest_path), '-q', '--disable-warnings', '--junitxml', str(junit_path)
    ]
    print('Running:', ' '.join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode not in (0, 1):
        # pytest returns 0 for success, 1 for failures
        print('pytest failed to run properly:', res.stderr)

    if not junit_path.exists():
        print('junit xml not found, skipping auto-populate')
        return {}

    tree = ET.parse(junit_path)
    root = tree.getroot()

    results = {}
    # junit format: testsuite/testcase, testcase name contains param info
    for testcase in root.findall('.//testcase'):
        name = testcase.get('name')
        # detect failure child
        failed = testcase.find('failure') is not None or testcase.find('error') is not None
        # extract bracketed params if present
        m = re.search(r"\[(.*)\]", name)
        key = None
        if m:
            params = m.group(1)
            # params are usually separated by '-'
            # e.g. 1-closed-True or 1-closed-True-0
            parts = [p.strip() for p in re.split(r"-", params)]
            # try to get booking_id and status
            if len(parts) >= 2:
                booking_id = parts[0]
                status = parts[1]
                key = (booking_id, status)
        else:
            # fallback: use entire name
            key = (name,)

        results[key] = {'failed': failed, 'name': name}

    return results


def make_workbook(rows, pytest_results):
    wb = Workbook()
    ws = wb.active
    ws.title = 'update_booking_status'

    headers = ['Test case ID', 'Description', 'Prior condition', 'Input data', 'Step', 'Expected result', 'Actual result', 'Status']
    ws.append(headers)

    for i, r in enumerate(rows, start=1):
        tc_id = f"TC-{i:03d}"
        booking_id = r.get('booking_id')
        status = r.get('status')
        expected = r.get('expected_result')

        description = f"Update booking #{booking_id} to status '{status}'"
        prior = "Booking exists with previous known status" if booking_id in ('1', '2', '3') else "Booking may not exist"
        input_data = f"booking_id={booking_id}, status={status}"
        step = "Call update_booking_status(booking_id, status)"
        expected_result = 'True' if expected.lower() in ('true', '1', 'yes') else 'False'

        key = (booking_id, status)
        res = pytest_results.get(key)
        if res is None:
            actual_result = 'Not executed'
            status_cell = 'Not run'
        else:
            if not res['failed']:
                # test passed -> actual equals expected
                actual_result = expected_result
                status_cell = 'Pass'
            else:
                actual_result = 'Mismatch'
                status_cell = 'Fail'

        ws.append([tc_id, description, prior, input_data, step, expected_result, actual_result, status_cell])

    return wb


def main():
    if not CSV_PATH.exists():
        print(f"CSV not found at {CSV_PATH}")
        return 2

    rows = load_csv(CSV_PATH)

    # run pytest and gather results
    pytest_results = run_pytest_and_get_results(PYTEST_FILE)

    wb = make_workbook(rows, pytest_results)
    wb.save(OUTPUT_XLSX)
    print(f"Wrote Excel summary to {OUTPUT_XLSX}")
    return 0


if __name__ == '__main__':
    import sys
    raise SystemExit(main())
