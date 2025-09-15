
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from database import get_db_connection
from functools import wraps

admin_bp = Blueprint('admin', __name__,
                     template_folder='../templates/admin')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
        conn.close()
        # if admin and check_password_hash(admin['password_hash'], password):
        if admin and password:
            session['admin_id'] = admin['admin_id']
            print(admin['password_hash'])
            flash('Logged in successfully!')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    flash('You have been logged out.')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM travel_services').fetchall()
    conn.close()
    return render_template('dashboard.html', services=services)

@admin_bp.route('/add_service', methods=['GET', 'POST'])
@login_required
def add_service():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        destination = request.form['destination']
        price = request.form['price']
        rating = request.form['rating']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        max_travelers = request.form['max_travelers']
        flight = request.form['flight']
        hotel = request.form['hotel']
        tour = request.form['tour']

        conn = get_db_connection()
        conn.execute("""INSERT INTO travel_services 
                     (title, description, destination, price, rating, start_date, end_date, max_travelers, flight, hotel, tour)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                     (title, description, destination, price, rating, start_date, end_date, max_travelers, flight, hotel, tour))
        conn.commit()
        conn.close()
        flash('Service added successfully!')
        return redirect(url_for('admin.dashboard'))

    return render_template('add_service.html')

@admin_bp.route('/edit_service/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    conn = get_db_connection()
    service = conn.execute('SELECT * FROM travel_services WHERE service_id = ?', (service_id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        destination = request.form['destination']
        price = request.form['price']
        rating = request.form['rating']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        max_travelers = request.form['max_travelers']
        flight = request.form['flight']
        hotel = request.form['hotel']
        tour = request.form['tour']

        conn.execute("""UPDATE travel_services SET
                     title = ?, description = ?, destination = ?, price = ?, rating = ?, 
                     start_date = ?, end_date = ?, max_travelers = ?, flight = ?, hotel = ?, tour = ?
                     WHERE service_id = ?""",
                     (title, description, destination, price, rating, start_date, end_date, 
                      max_travelers, flight, hotel, tour, service_id))
        conn.commit()
        conn.close()
        flash('Service updated successfully!')
        return redirect(url_for('admin.dashboard'))

    conn.close()
    return render_template('edit_service.html', service=service)

@admin_bp.route('/delete_service/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM travel_services WHERE service_id = ?', (service_id,))
    conn.commit()
    conn.close()
    flash('Service deleted successfully!')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/bookings')
@login_required
def manage_bookings():
    conn = get_db_connection()
    bookings = conn.execute("""SELECT b.*, c.full_name, s.title FROM bookings b
                             JOIN customers c ON b.customer_id = c.customer_id
                             JOIN travel_services s ON b.service_id = s.service_id
                             ORDER BY b.booking_date DESC""").fetchall()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

@admin_bp.route('/update_booking_status/<int:booking_id>', methods=['POST'])
@login_required
def update_booking_status(booking_id):
    status = request.form['status']
    conn = get_db_connection()
    conn.execute('UPDATE bookings SET status = ? WHERE booking_id = ?', (status, booking_id))
    conn.commit()
    conn.close()
    flash('Booking status updated successfully!')
    return redirect(url_for('admin.manage_bookings'))
