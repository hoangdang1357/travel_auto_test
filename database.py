
import sqlite3
from werkzeug.security import generate_password_hash
from flask import current_app, g
from alter_table import apply_migrations

def get_db_connection():
    if 'db' not in g:
        db_name = current_app.config.get('DATABASE', 'travel.db')
        g.db = sqlite3.connect(db_name)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db_connection()
    # Drop all tables for a clean slate
    db.executescript("""
        DROP TABLE IF EXISTS reviews;
        DROP TABLE IF EXISTS payments;
        DROP TABLE IF EXISTS traveler_details;
        DROP TABLE IF EXISTS bookings;
        DROP TABLE IF EXISTS travel_services;
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS admins;
    """)
    with current_app.open_resource('database.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    # Apply migrations
    apply_migrations(db)

def init_app(app):
    app.teardown_appcontext(close_db)

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

def add_sample_admin():
    conn = get_db_connection()
    password_hash = generate_password_hash('admin')
    conn.execute('INSERT INTO admins (username, password_hash, email) VALUES (?, ?, ?)',
                 ('admin', password_hash, 'admin@example.com'))
    conn.commit()

if __name__ == '__main__':
    from app import app
    with app.app_context():
        init_db()
        add_sample_data()
        add_sample_admin()
        print("Database initialized and sample data added.")

