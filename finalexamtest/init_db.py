import sqlite3

DB_PATH = "travel_booking.db"

# Kết nối tới database (nếu chưa có thì sẽ tạo mới)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Tạo bảng customers
cur.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT
)
""")

# Thêm dữ liệu mẫu



conn.commit()
conn.close()

print("Database initialized with sample data!")
