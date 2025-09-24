# utils/validation.py
from datetime import datetime, date
VALID_STATUSES = {"pending", "confirmed", "cancelled"}

def calculate_total_amount(price, travelers, tax=0.0, discount=0.0):
    try:
        price = float(price)
    except (TypeError, ValueError):
        raise ValueError("price must be a number")
    try:
        travelers = int(travelers)
    except (TypeError, ValueError):
        raise ValueError("travelers must be an integer")

    if price <= 0:
        raise ValueError("price must be > 0")
    if travelers <= 0:
        raise ValueError("travelers must be > 0")
    try:
        tax = float(tax)
        discount = float(discount)
    except (TypeError, ValueError):
        raise ValueError("tax and discount must be numbers")

    if not (0 <= tax <= 1):
        raise ValueError("tax must be between 0 and 1")
    if not (0 <= discount <= 1):
        raise ValueError("discount must be between 0 and 1")

    subtotal = price * travelers
    subtotal_after_discount = subtotal * (1 - discount)
    total = subtotal_after_discount * (1 + tax)
    return round(total, 2)


def validate_travel_dates(start_date_str, end_date_str):
    if not start_date_str or not end_date_str:
        raise ValueError("start and end dates must be provided")
    try:
        start = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except Exception:
        raise ValueError("dates must be in YYYY-MM-DD format")
    if end <= start:
        return False
    return True


def validate_login(username, password, users_db=None):
    if username is None or password is None:
        raise ValueError("username and password must be provided")
    if not isinstance(username, str) or not isinstance(password, str):
        raise ValueError("username and password must be strings")
    username = username.strip()
    password = password.strip()
    if username == "" or password == "": 
        return False
    if len(username) >= 256:
        raise ValueError("username too long")
    if len(password) < 3:
        raise ValueError("password too short")
    if users_db is None:
        users_db = {"admin": "1234"}
    expected = users_db.get(username)
    if expected is None:
        return False
    return expected == password


def update_booking_status(booking_id, status, bookings_db=None):
    if booking_id is None:
        raise ValueError("booking_id must be provided")
    try:
        booking_id = int(booking_id)
    except (TypeError, ValueError):
        raise ValueError("booking_id must be an integer")
    if booking_id <= 0:
        raise ValueError("booking_id must be > 0")
    if status is None:
        raise ValueError("status must be provided")
    if not isinstance(status, str) or status.strip() == "":
        raise ValueError("status must be a non-empty string")
    status_lower = status.strip().lower()
    if status_lower not in VALID_STATUSES:
        raise ValueError("invalid status")
    if bookings_db is not None:
        if booking_id not in bookings_db:
            raise ValueError("booking_id not found")
        bookings_db[booking_id]['status'] = status_lower
    return status_lower
