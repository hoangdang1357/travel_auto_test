
import sqlite3
from werkzeug.security import generate_password_hash

def get_db_connection():
    conn = sqlite3.connect('travel.db')
    conn.row_factory = sqlite3.Row
    return conn

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
    print("Database initialized and sample data added.")
