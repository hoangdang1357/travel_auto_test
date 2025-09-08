from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

# ===========================
# Cấu hình
# ===========================
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or "dev_secret"  # nếu chưa có .env thì dùng mặc định

DB_PATH = "travel_booking.db"

# cấu hình cho SQLAlchemy (chưa dùng ở đây, nhưng để sẵn)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Tài khoản admin mặc định
ADMIN_USERNAME = "admin@123"
ADMIN_PASSWORD = "123"

# ===========================
# Helper
# ===========================
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Decorator để bảo vệ route admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['username'] != ADMIN_USERNAME:
            flash("You must be an admin to access this page.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ===========================
# Routes chính
# ===========================
@app.route('/')
def index():
    conn = get_db_connection()
    tours = conn.execute("SELECT * FROM travel_services WHERE tour IS NOT NULL").fetchall()
    conn.close()
    return render_template("home.html", tours=tours)

@app.route('/tour/<int:service_id>')
def tour_detail(service_id):
    conn = get_db_connection()
    tour = conn.execute("SELECT * FROM travel_services WHERE service_id = ?", (service_id,)).fetchone()
    conn.close()
    if tour is None:
        return "Tour not found", 404
    return render_template("tour_detail.html", tour=tour)

# ===========================
# Travel Services CRUD
# ===========================
@app.route('/manage_travel_services')
@admin_required
def manage_travel_services():
    conn = get_db_connection()
    services = conn.execute("SELECT * FROM travel_services").fetchall()
    conn.close()
    return render_template("travel_services/manage_travel_services.html", services=services)

@app.route('/add_travel_service', methods=['POST'])
def add_travel_service():
    service_id = request.form.get('service_id')
    title = request.form['title']
    destination = request.form.get('destination')
    price = request.form['price']
    rating = request.form.get('rating')
    flight = request.form.get('flight')
    hotel = request.form.get('hotel')
    tour = request.form.get('tour')
    max_travelers = request.form.get('max_travelers')

    conn = get_db_connection()
    if service_id:  # edit
        conn.execute("""UPDATE travel_services 
                        SET title=?, destination=?, price=?, rating=?, flight=?, hotel=?, tour=?, max_travelers=? 
                        WHERE service_id=?""",
                     (title, destination, price, rating, flight, hotel, tour, max_travelers, service_id))
    else:  # add new
        conn.execute("""INSERT INTO travel_services 
                        (title,destination,price,rating,flight,hotel,tour,max_travelers) 
                        VALUES (?,?,?,?,?,?,?,?)""",
                     (title,destination,price,rating,flight,hotel,tour,max_travelers))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_travel_services'))

@app.route('/delete_travel_service/<int:service_id>')
def delete_travel_service(service_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM travel_services WHERE service_id=?", (service_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_travel_services'))

@app.route('/edit_travel_service/<int:service_id>', methods=['POST'])
def edit_travel_service(service_id):
    title = request.form['title']
    destination = request.form.get('destination')
    price = request.form['price']
    rating = request.form.get('rating')
    flight = request.form.get('flight')
    hotel = request.form.get('hotel')
    tour = request.form.get('tour')
    max_travelers = request.form.get('max_travelers')

    conn = get_db_connection()
    conn.execute("""UPDATE travel_services 
                    SET title=?, destination=?, price=?, rating=?, flight=?, hotel=?, tour=?, max_travelers=? 
                    WHERE service_id=?""",
                 (title, destination, price, rating, flight, hotel, tour, max_travelers, service_id))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_travel_services'))

# ===========================
# Bookings CRUD
# ===========================
@app.route('/manage_bookings')
@admin_required
def manage_bookings():
    conn = get_db_connection()
    bookings = conn.execute("""
        SELECT b.booking_id, b.travel_date, b.num_travelers, b.status, b.total_amount,
               c.customer_id, c.full_name AS customer_name,
               s.service_id, s.title AS service_title
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        JOIN travel_services s ON b.service_id = s.service_id
        ORDER BY b.booking_id DESC
    """).fetchall()

    customers = conn.execute("SELECT customer_id, full_name FROM customers").fetchall()
    services = conn.execute("SELECT service_id, title FROM travel_services").fetchall()
    conn.close()

    return render_template("bookings/manage_bookings.html",
                           bookings=bookings, customers=customers, services=services)

@app.route('/add_booking', methods=['POST'])
def add_booking():
    customer_id = request.form['customer_id']
    service_id = request.form['service_id']
    travel_date = request.form['travel_date']
    num_travelers = request.form['num_travelers']
    status = request.form['status']
    total_amount = request.form['total_amount']

    conn = get_db_connection()
    conn.execute("""INSERT INTO bookings 
                    (customer_id, service_id, travel_date, num_travelers, status, total_amount)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                 (customer_id, service_id, travel_date, num_travelers, status, total_amount))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_bookings'))

@app.route('/edit_booking/<int:booking_id>', methods=['POST'])
def edit_booking(booking_id):
    customer_id = request.form['customer_id']
    service_id = request.form['service_id']
    travel_date = request.form['travel_date']
    num_travelers = request.form['num_travelers']
    status = request.form['status']
    total_amount = request.form['total_amount']

    conn = get_db_connection()
    conn.execute("""UPDATE bookings
                    SET customer_id=?, service_id=?, travel_date=?, num_travelers=?, status=?, total_amount=?
                    WHERE booking_id=?""",
                 (customer_id, service_id, travel_date, num_travelers, status, total_amount, booking_id))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_bookings'))

@app.route('/delete_booking/<int:booking_id>')
def delete_booking(booking_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM bookings WHERE booking_id=?", (booking_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_bookings'))

# ===========================
# Customers CRUD (sqlite3)
# ===========================
@app.route('/manage_customers')
@admin_required
def manage_customers():
    conn = get_db_connection()
    customers = conn.execute("SELECT * FROM customers").fetchall()
    conn.close()
    return render_template("customers/manage_customers.html", customers=customers)

@app.route("/customers/add", methods=["POST"])
def add_customer():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]

    conn = get_db_connection()
    conn.execute("INSERT INTO customers (full_name, email, phone) VALUES (?, ?, ?)",
                 (name, email, phone))
    conn.commit()
    conn.close()
    flash("Customer added successfully!", "success")
    return redirect(url_for("manage_customers"))

@app.route("/customers/edit/<int:id>", methods=["POST"])
def edit_customer(id):
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]

    conn = get_db_connection()
    conn.execute("UPDATE customers SET full_name=?, email=?, phone=? WHERE customer_id=?",
                 (name, email, phone, id))
    conn.commit()
    conn.close()
    flash("Customer updated successfully!", "success")
    return redirect(url_for("manage_customers"))

@app.route("/customers/delete/<int:id>")
def delete_customer(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM customers WHERE customer_id=?", (id,))
    conn.commit()
    conn.close()
    flash("Customer deleted!", "danger")
    return redirect(url_for("manage_customers"))

# ===========================
# Auth routes
# ===========================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO customers (full_name, email, password_hash) VALUES (?, ?, ?)",
                (full_name, email, hashed_password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Email already registered!")
            conn.close()
            return redirect(url_for('register'))

        conn.close()
        flash("Registration successful! Please login.")
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['username'] = ADMIN_USERNAME
            flash("Admin login successful!")
            return redirect(url_for('home_admin'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/home_admin')
def home_admin():
    if 'username' in session:
        return render_template("home_admin.html")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('login'))

# ===========================
# Run app
# ===========================
if __name__ == "__main__":
    app.run(debug=True)
