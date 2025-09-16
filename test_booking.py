import pytest
from datetime import date, timedelta

# ====== Hàm cần test ======

def calculate_price(base, tax, discount):
    return base + tax - discount

def validate_dates(start_date, end_date):
    return start_date < end_date

def validate_login(username, password, users):
    return users.get(username) == password

def update_booking_status(booking, new_status):
    if not isinstance(new_status, str):
        raise ValueError("Status must be a string")
    booking["status"] = new_status
    return booking


# ====== Unit Tests ======

# --- calculate_price ---
def test_calculate_price():
    assert calculate_price(100, 10, 5) == 105
    assert calculate_price(200, 20, 50) == 170
    assert calculate_price(0, 0, 0) == 0

def test_calculate_price_fail_expected_wrong():
    # Cố tình mong đợi sai -> FAIL
    assert calculate_price(100, 10, 20) == 95


# --- validate_dates ---
def test_validate_dates():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)

    assert validate_dates(today, tomorrow) is True
    assert validate_dates(tomorrow, today) is False
    assert validate_dates(today, today) is False

def test_validate_dates_type_error():
    # Truyền sai kiểu dữ liệu -> ERROR
    with pytest.raises(TypeError):
        validate_dates("2025-01-01", "2025-01-02")


# --- validate_login ---
def test_validate_login():
    fake_users = {"admin": "1234", "user": "abcd"}

    assert validate_login("admin", "1234", fake_users) is True
    assert validate_login("user", "abcd", fake_users) is True
    assert validate_login("user", "wrong", fake_users) is False
    assert validate_login("ghost", "1234", fake_users) is False


# --- update_booking_status ---
def test_update_booking_status():
    booking = {"id": 1, "status": "pending"}

    updated = update_booking_status(booking, "confirmed")
    assert updated["status"] == "confirmed"

    updated = update_booking_status(booking, "cancelled")
    assert updated["status"] == "cancelled"

def test_update_status_invalid_type():
    booking = {"id": 6, "status": "pending"}
    # Truyền kiểu int thay vì string -> ERROR
    with pytest.raises(ValueError):
        update_booking_status(booking, 123)
def test_calculate_price_negative_values():
    # Giá trị âm không hợp lệ
    with pytest.raises(ValueError):
        calculate_price(-100, 10, 5)

def test_calculate_price_high_discount():
    # Discount lớn hơn base price => giá không được âm
    price = calculate_price(100, 10, 200)
    assert price >= 0

def test_validate_dates_same_day():
    # Ngày đi = ngày về => hợp lệ
    today = datetime.now().date()
    assert validate_dates(today, today) is True

def test_validate_login_empty_username():
    # Username trống => không hợp lệ
    assert validate_login("", "password123") is False

def test_update_booking_status_invalid_value():
    # Truyền status không hợp lệ => báo lỗi
    booking = {"id": 10, "status": "pending"}
    with pytest.raises(ValueError):
        update_booking_status(booking, new_status="unknown")