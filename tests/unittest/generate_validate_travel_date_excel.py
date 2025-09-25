import csv
import re
import tempfile
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from openpyxl import Workbook
import sys


CSV_PATH = Path(__file__).parent / 'csv_unit_testing' / 'validate_travel_date.csv'
OUTPUT_XLSX = Path(__file__).parent / 'validate_travel_date_summary.xlsx'
PYTEST_FILE = Path(__file__).parent / 'test_validate_travel_date.py'


def load_csv(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def run_pytest_and_get_results(pytest_path):
    with tempfile.NamedTemporaryFile(prefix='junit-', suffix='.xml', delete=False) as tmp:
        junit_path = Path(tmp.name)

    cmd = [
        str(Path(sys.executable)), '-m', 'pytest', str(pytest_path), '-q', '--disable-warnings', '--junitxml', str(junit_path)
    ]
    print('Running:', ' '.join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode not in (0, 1):
        print('pytest failed to run properly:', res.stderr)

    if not junit_path.exists():
        print('junit xml not found, skipping auto-populate')
        return {}

    tree = ET.parse(junit_path)
    root = tree.getroot()

    results = {}
    for testcase in root.findall('.//testcase'):
        name = testcase.get('name')
        failed = testcase.find('failure') is not None or testcase.find('error') is not None
        # name usually contains index or parameters in brackets; for this test it may not
        # We'll try to match the input_date value if present
        m = re.search(r"\[(.*)\]", name)
        key = None
        if m:
            params = m.group(1)
            key = (params,)
        else:
            key = (name,)

        results[key] = {'failed': failed, 'name': name}

    return results


def make_workbook(rows, pytest_results):
    wb = Workbook()
    ws = wb.active
    ws.title = 'validate_travel_date'

    headers = ['Test case ID', 'Description', 'Prior condition', 'Input data', 'Step', 'Expected result', 'Actual result', 'Status']
    ws.append(headers)

    for i, r in enumerate(rows, start=1):
        tc_id = f"TC-{i:03d}"
        input_date = r.get('input_date')
        expected_valid = r.get('expected_valid')
        expected_message = r.get('expected_message')

        description = f"validate_travel_date('{input_date}')"
        prior = 'N/A'  # pure validation function
        input_data = f"input_date={input_date}"
        step = 'Call validate_travel_date(input_date)'
        expected_result = f"{expected_valid} => '{expected_message}'"

        # Attempt to match pytest testcase by input string in testcase name
        match_key = None
        for k in pytest_results.keys():
            if input_date in ''.join(k):
                match_key = k
                break

        if match_key is None:
            actual_result = 'Not executed'
            status_cell = 'Not run'
        else:
            res = pytest_results[match_key]
            if not res['failed']:
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
    pytest_results = run_pytest_and_get_results(PYTEST_FILE)
    wb = make_workbook(rows, pytest_results)
    wb.save(OUTPUT_XLSX)
    print(f"Wrote Excel summary to {OUTPUT_XLSX}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
