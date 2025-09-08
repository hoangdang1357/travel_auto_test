
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db_connection
from functools import wraps
import datetime

booking_bp = Blueprint('booking', __name__,
                       template_folder='../templates/booking')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'customer_id' not in session:
            return redirect(url_for('auth.signin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@booking_bp.route('/new/<int:service_id>', methods=['GET', 'POST'])
@login_required
def new_booking(service_id):
    conn = get_db_connection()
    service = conn.execute('SELECT * FROM travel_services WHERE service_id = ?', (service_id,)).fetchone()

    if request.method == 'POST':
        travel_date = request.form['travel_date']
        num_travelers = int(request.form['num_travelers'])
        customer_id = session['customer_id']
        total_amount = service['price'] * num_travelers

        booking = conn.execute("""INSERT INTO bookings (customer_id, service_id, travel_date, num_travelers, total_amount)
                     VALUES (?, ?, ?, ?, ?)""",
                     (customer_id, service_id, travel_date, num_travelers, total_amount))
        conn.commit()
        booking_id = booking.lastrowid
        conn.close()

        flash('Booking created successfully! Please provide traveler details.')
        return redirect(url_for('booking.traveler_details', booking_id=booking_id))

    conn.close()
    return render_template('new.html', service=service)

@booking_bp.route('/traveler_details/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def traveler_details(booking_id):
    if request.method == 'POST':
        # In a real application, you would loop through the number of travelers
        full_name = request.form['full_name']
        gender = request.form['gender']
        dob = request.form['dob']
        passport_number = request.form['passport_number']

        conn = get_db_connection()
        conn.execute("""INSERT INTO traveler_details (booking_id, full_name, gender, dob, passport_number)
                     VALUES (?, ?, ?, ?, ?)""",
                     (booking_id, full_name, gender, dob, passport_number))
        conn.commit()
        conn.close()

        flash('Traveler details saved successfully! Proceed to payment.')
        return redirect(url_for('booking.payment', booking_id=booking_id))

    return render_template('traveler_details.html', booking_id=booking_id)

@booking_bp.route('/payment/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def payment(booking_id):
    conn = get_db_connection()
    booking = conn.execute('SELECT * FROM bookings WHERE booking_id = ?', (booking_id,)).fetchone()

    if request.method == 'POST':
        payment_method = request.form['payment_method']
        amount = booking['total_amount']

        conn.execute("""INSERT INTO payments (booking_id, payment_method, amount, status, transaction_ref)
                     VALUES (?, ?, ?, ?, ?)""",
                     (booking_id, payment_method, amount, 'paid', f'txn_{booking_id}_{datetime.datetime.now().timestamp()}'))
        
        conn.execute('UPDATE bookings SET status = ? WHERE booking_id = ?', ('confirmed', booking_id))
        conn.commit()
        conn.close()

        flash('Payment successful! Your booking is confirmed.')
        return redirect(url_for('booking.history'))

    conn.close()
    return render_template('payment.html', booking=booking)

@booking_bp.route('/history')
@login_required
def history():
    customer_id = session['customer_id']
    conn = get_db_connection()
    bookings = conn.execute("""SELECT b.*, s.title FROM bookings b 
                             JOIN travel_services s ON b.service_id = s.service_id
                             WHERE b.customer_id = ? ORDER BY b.booking_date DESC""", (customer_id,)).fetchall()
    conn.close()
    return render_template('history.html', bookings=bookings)
