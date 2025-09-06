import sqlite3

# Kết nối hoặc tạo cơ sở dữ liệu
conn = sqlite3.connect("travel_booking.db")
cursor = conn.cursor()

# Kích hoạt khóa ngoại
cursor.execute("PRAGMA foreign_keys = ON;")

# ===========================
# Tạo bảng
# ===========================

# Xóa các bảng theo thứ tự an toàn
tables = ["reviews", "payments", "traveler_details", "bookings", "travel_services", "customers", "admins"]
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# Bảng Admins
cursor.execute("""
CREATE TABLE admins (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")

# Bảng Customers
cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone TEXT,
    address TEXT
)
""")

# Bảng Travel Services
cursor.execute("""
CREATE TABLE travel_services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    price NUMERIC NOT NULL,
    rating NUMERIC,
    destination TEXT,
    flight TEXT,
    hotel TEXT,
    tour TEXT,
    max_travelers INT,
    title TEXT NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Bảng Bookings
cursor.execute("""
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INT NOT NULL,
    service_id INT NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    travel_date DATE NOT NULL,
    num_travelers INT DEFAULT 1,
    status TEXT CHECK(status IN ('pending','confirmed','canceled')) DEFAULT 'pending',
    total_amount NUMERIC NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES travel_services(service_id) ON DELETE CASCADE
)
""")

# Bảng Traveler Details
cursor.execute("""
CREATE TABLE traveler_details (
    traveler_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INT NOT NULL,
    full_name TEXT NOT NULL,
    gender TEXT CHECK(gender IN ('male','female','other')),
    dob DATE,
    passport_number TEXT,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
)
""")

# Bảng Payments
cursor.execute("""
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INT NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method TEXT CHECK(payment_method IN ('credit_card','e_wallet','gateway')),
    amount NUMERIC NOT NULL,
    status TEXT CHECK(status IN ('pending','paid','failed')) DEFAULT 'pending',
    transaction_ref TEXT UNIQUE,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
)
""")

# Bảng Reviews
cursor.execute("""
CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INT NOT NULL,
    service_id INT NOT NULL,
    rating INT,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES travel_services(service_id) ON DELETE CASCADE
)
""")


# ===========================
# Commit và đóng kết nối
# ===========================
conn.commit()
conn.close()

print("Database and tables created successfully!")
