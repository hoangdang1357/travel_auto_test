import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
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

    # Dữ liệu mẫu
    cur.execute("DELETE FROM customers")  # clear cũ nếu có
    cur.executemany(
        "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
        [
            ("Alice", "alice@example.com", "123456789"),
            ("Bob", "bob@example.com", "987654321"),
            ("Charlie", "charlie@example.com", "555666777"),
        ],
    )

    conn.commit()
    conn.close()
    print("✅ Database initialized with sample data!")

if __name__ == "__main__":
    init_db()
