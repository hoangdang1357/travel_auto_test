import csv
from pathlib import Path
from openpyxl import Workbook
import sys

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from booking.routes import calculate_total_amount


CSV_PATH = Path(__file__).parent / 'csv_unit_testing' / 'calculate_total_price.csv'
OUTPUT_XLSX = Path(__file__).parent / 'calculate_total_price_summary.xlsx'


def load_csv(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def make_workbook(rows):
    wb = Workbook()
    ws = wb.active
    ws.title = 'calculate_total_price'

    headers = ['Test case ID', 'Module', 'Description', 'Prior condition', 'Input data', 'Step', 'Expected result', 'Actual result', 'Status']
    ws.append(headers)

    for i, r in enumerate(rows, start=1):
        tc_id = f"TC-{i:03d}"
        price = float(r.get('price', 0))
        num_travelers = int(r.get('num_travelers', 0))
        tax = float(r.get('tax', 0.0)) if r.get('tax') not in (None, '') else 0.0
        discount = float(r.get('discount', 0.0)) if r.get('discount') not in (None, '') else 0.0
        expected = float(r.get('expected', 0.0))

        description = f"calculate_total_amount(price={price}, num_travelers={num_travelers}, tax={tax}, discount={discount})"
        prior = 'N/A'
        input_data = f"price={price}, num_travelers={num_travelers}, tax={tax}, discount={discount}"
        step = 'Call calculate_total_amount with inputs'

        # Compute actual by calling function directly
        try:
            actual_value = calculate_total_amount(price, num_travelers, tax, discount)
            actual_result = str(actual_value)
            status = 'Pass' if abs(actual_value - expected) < 1e-9 else 'Fail'
        except Exception as e:
            actual_result = f'EXCEPTION: {e}'
            status = 'Fail'

        ws.append([tc_id, 'booking.routes', description, prior, input_data, step, str(expected), actual_result, status])

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
