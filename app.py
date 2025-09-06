from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# ===========================
# Cấu hình
# ===========================
app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Đổi thành secret key mạnh

DB_PATH = "travel_booking.db"

# ===========================
# Helper function
# ===========================
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ===========================
# Route cơ bản
# ===========================

@app.route('/')
def index():
    conn = get_db_connection()
    tours = conn.execute("SELECT * FROM travel_services WHERE tour IS NOT NULL").fetchall()
    conn.close()
    return render_template("index.html", tours=tours)

@app.route('/tour/<int:service_id>')
def tour_detail(service_id):
    conn = get_db_connection()
    tour = conn.execute("SELECT * FROM travel_services WHERE service_id = ?", (service_id,)).fetchone()
    conn.close()
    if tour is None:
        return "Tour not found", 404
    return render_template("tour_detail.html", tour=tour)

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
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM customers WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['customer_id']
            session['full_name'] = user['full_name']
            flash("Login successful!")
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password.")
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('index'))

# ===========================
# Run app
# ===========================
if __name__ == "__main__":
    app.run(debug=True)
