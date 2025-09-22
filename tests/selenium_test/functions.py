# functions.py
import datetime

# ---- Câu 1: Tính tổng tiền booking ----
def calculate_total_amount(price, travelers):
    if not isinstance(price, (int, float)) or not isinstance(travelers, int):
        raise TypeError("Price must be numeric and travelers must be int")
    return price * travelers

# ---- Câu 2: Validate ngày đi ----
def validate_travel_date(date_str):
    if not date_str:
        return False, "Date is required"
    try:
        travel_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return False, "Invalid date format"
    if travel_date <= datetime.date.today():
        return False, "Travel date cannot be in the past"
    return True, ""

# ---- Câu 3: Cập nhật trạng thái booking ----
def update_booking_status(booking_id, status):
    if not isinstance(booking_id, int) or booking_id <= 0:
        return False, "Invalid booking ID"
    if status not in ["pending", "confirmed", "cancelled"]:
        return False, "Invalid status"
    return True, "Status updated"

# ---- Câu 4: Validate thông tin đăng nhập ----
def validate_login_credentials(email, password):
    if not email or not password:
        return False, "Email and password are required"
    if "@" not in email or "." not in email:
        return False, "Invalid email format"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, ""
