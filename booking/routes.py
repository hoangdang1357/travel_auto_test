from datetime import datetime


def calculate_booking_price(base_price, num_travelers, tax_rate, discount):
    if not isinstance(base_price, (int, float)) or not isinstance(num_travelers, int) \
       or not isinstance(tax_rate, (int, float)) or not isinstance(discount, (int, float)):
        raise TypeError("Invalid input type")

    if num_travelers < 1:
        raise ValueError("Number of travelers must be >= 1")

    if tax_rate < 0 or tax_rate > 1:
        raise ValueError("Tax rate must be between 0 and 1")

    subtotal = base_price * num_travelers
    total_after_tax = subtotal + (subtotal * tax_rate)

    if discount < 0 or discount > total_after_tax:
        raise ValueError("Invalid discount")

    final_price = total_after_tax - discount
    return round(final_price, 2)


def validate_travel_date(date_str):
    if not date_str:
        return False, "required"

    try:
        travel_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return False, "Invalid date format"

    today = datetime.today().date()
    if travel_date < today:
        return False, "past"

    return True, ""


def update_booking_status(current_status, new_status):
    valid_status = {"pending", "confirmed", "cancelled"}

    if new_status not in valid_status:
        return current_status

    if current_status == "cancelled":
        return "cancelled"

    return new_status
