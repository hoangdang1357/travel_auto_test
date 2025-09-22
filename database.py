
import sqlite3
from werkzeug.security import generate_password_hash

def get_db_connection():
    conn = sqlite3.connect('travel.db')
    conn.row_factory = sqlite3.Row
    return conn

def column_exists(cur: sqlite3.Cursor, table: str, column: str) -> bool:
    """Check if a column exists in a table"""
    cur.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cur.fetchall())

def add_column_if_missing(cur: sqlite3.Cursor, table: str, column_name: str, column_def: str) -> None:
    """Add a column to a table if it doesn't already exist"""
    if column_exists(cur, table, column_name):
        print(f"Column '{column_name}' already exists on '{table}', skipping")
        return
    sql = f"ALTER TABLE {table} ADD COLUMN {column_name} {column_def}"
    print(f"Applying: {sql}")
    cur.execute(sql)

def migrate_database():
    """Apply database migrations for existing databases"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    
    # Add verification columns to customers table (from alter_table.py)
    add_column_if_missing(cur, "customers", "verified", "INTEGER DEFAULT 0")
    add_column_if_missing(cur, "customers", "verification_code", "TEXT DEFAULT ''")
    add_column_if_missing(cur, "customers", "code_expiry", "DATETIME DEFAULT NULL")
    
    conn.commit()
    conn.close()
    print("Database migration completed.")

def init_db():
    conn = get_db_connection()
    with open('database.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def add_sample_data():
    conn = get_db_connection()
    # Sample data for travel_services
    services = [
        (199.99, 4.5, 'Paris, France', 'Flight B737', 'Hotel Paris', 'Eiffel Tower Tour', 20, 'A trip to Paris', 'A beautiful trip to the city of love', '2025-10-20', '2025-10-27'),
        (299.99, 4.8, 'Tokyo, Japan', 'Flight A380', 'Hotel Tokyo', 'Shibuya Crossing Tour', 15, 'A trip to Tokyo', 'Experience the vibrant culture of Tokyo', '2025-11-10', '2025-11-18'),
        (150.00, 4.2, 'New York, USA', 'Flight B787', 'Hotel New York', 'Statue of Liberty Tour', 25, 'A trip to New York', 'Explore the city that never sleeps', '2025-12-01', '2025-12-08')
    ]
    conn.executemany("""
    INSERT INTO travel_services (price, rating, destination, flight, hotel, tour, max_travelers, title, description, start_date, end_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, services)
    conn.commit()
    conn.close()

def add_sample_admin():
    conn = get_db_connection()
    password_hash = generate_password_hash('admin')
    conn.execute('INSERT INTO admins (username, password_hash, email) VALUES (?, ?, ?)',
                 ('admin', password_hash, 'admin@example.com'))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    add_sample_data()
    add_sample_admin()
    migrate_database()  # Apply any pending migrations
    print("Database initialized, sample data added, and migrations applied.")
