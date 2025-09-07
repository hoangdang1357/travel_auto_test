import sqlite3
from werkzeug.security import generate_password_hash

from datetime import date

# Kết nối database
conn = sqlite3.connect('travel_booking.db')
cursor = conn.cursor()

# Sample data cho travel_services
sample_services = [
    {
        "price": 1200,
        "rating": 4.5,
        "destination": "Paris, France",
        "flight": "AF123",
        "hotel": None,
        "tour": None,
        "max_travelers": 30,
        "title": "Flight to Paris",
        "description": "Direct flight to Paris with in-flight meals",
        "start_date": "2025-10-01",
        "end_date": "2025-10-01"
    },
    {
        "price": 800,
        "rating": 4.2,
        "destination": "Tokyo, Japan",
        "flight": None,
        "hotel": "Shinjuku Hotel",
        "tour": None,
        "max_travelers": 50,
        "title": "Hotel Stay in Tokyo",
        "description": "3 nights stay at 4-star Shinjuku Hotel",
        "start_date": "2025-11-01",
        "end_date": "2025-11-04"
    },
    {
        "price": 500,
        "rating": 4.8,
        "destination": "Hạ Long Bay, Vietnam",
        "flight": None,
        "hotel": None,
        "tour": "3-Day Cruise",
        "max_travelers": 20,
        "title": "Hạ Long Bay Tour",
        "description": "3-day cruise including meals and sightseeing",
        "start_date": "2025-12-10",
        "end_date": "2025-12-12"
    }
]

# Thêm dữ liệu vào bảng
for service in sample_services:
    cursor.execute("""
        INSERT INTO travel_services
        (price, rating, destination, flight, hotel, tour, max_travelers, title, description, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        service["price"],
        service["rating"],
        service["destination"],
        service["flight"],
        service["hotel"],
        service["tour"],
        service["max_travelers"],
        service["title"],
        service["description"],
        service["start_date"],
        service["end_date"]
    ))

# Sample data cho customers
sample_customers = [
    ("Nguyen Van A", "a@example.com", "123456"),
    ("Tran Thi B", "b@example.com", "123456"),
    ("Le Van C", "c@example.com", "123456"),
    ("Pham Thi D", "d@example.com", "123456"),
    ("Hoang Van E", "e@example.com", "123456"),
    ("Vu Thi F", "f@example.com", "123456"),
    ("Nguyen Van G", "g@example.com", "123456"),
    ("Tran Thi H", "h@example.com", "123456"),
    ("Le Van I", "i@example.com", "123456"),
    ("Pham Thi K", "k@example.com", "123456")
]

# Thêm dữ liệu vào bảng customers (tránh trùng email)
for name, email, password in sample_customers:
    password_hash = generate_password_hash(password)
    cursor.execute("""
        INSERT OR IGNORE INTO customers (full_name, email, password_hash)
        VALUES (?, ?, ?)
    """, (name, email, password_hash))


# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Sample data inserted successfully!")
