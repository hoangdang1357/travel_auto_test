import sqlite3

DATABASE = "travel_booking.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Tạo bảng customers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT
    )
    """)

    # Thêm dữ liệu mẫu nếu bảng đang trống
    cursor.execute("SELECT COUNT(*) FROM customers")
    count = cursor.fetchone()[0]
    if count == 0:
        sample_customers = [
            ("Nguyen Van A", "vana@example.com", "0901112222"),
            ("Tran Thi B", "thib@example.com", "0903334444"),
            ("Le Van C", "vanc@example.com", "0905556666")
        ]
        cursor.executemany(
            "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
            sample_customers
        )
        print("Inserted sample customers.")

    conn.commit()
    conn.close()
    print("Table 'customers' created successfully!")

if __name__ == "__main__":
    init_db()
