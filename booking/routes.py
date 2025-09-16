
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

def validate_travel_date(date_text):
    try:
        travel_date = datetime.datetime.strptime(date_text, '%Y-%m-%d').date()
        if travel_date < datetime.date.today():
            return False, "Travel date cannot be in the past."
        return True, ""
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD."

def validate_number_of_travelers(num_text):
    try:
        num = int(num_text)
        if num <= 0:
            return False, "Number of travelers must be a positive integer."
        return True, ""
    except ValueError:
        return False, "Number of travelers must be a valid integer."

def calculate_total_amount(price: float, num_travelers: int) -> float:
    return price * num_travelers

@booking_bp.route('/new/<int:service_id>', methods=['GET', 'POST'])
@login_required
def new_booking(service_id):
    conn = get_db_connection()
    service = conn.execute('SELECT * FROM travel_services WHERE service_id = ?', (service_id,)).fetchone()

    if request.method == 'POST':
        travel_date = request.form['travel_date']
        num_travelers = int(request.form['num_travelers'])
        customer_id = session['customer_id']
        total_amount = calculate_total_amount(service['price'], num_travelers)

        is_valid, error_message = validate_travel_date(travel_date)
        if not is_valid:
            flash(error_message)
            return render_template('new.html', service=service)
        
        is_valid, error_message = validate_number_of_travelers(request.form['num_travelers'])
        if not is_valid:
            flash(error_message)
            return render_template('new.html', service=service)

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
    conn = get_db_connection()
    booking = conn.execute('SELECT * FROM bookings WHERE booking_id = ?', (booking_id,)).fetchone()
    if not booking:
        conn.close()
        flash('Booking not found.')
        return redirect(url_for('services.index'))

    num_travelers = int(booking['num_travelers']) if booking['num_travelers'] is not None else 1

    if request.method == 'POST':
        # Expect arrays: full_name[], gender[], dob[], passport_number[]
        full_names = request.form.getlist('full_name[]') or request.form.getlist('full_name')
        genders = request.form.getlist('gender[]') or request.form.getlist('gender')
        dobs = request.form.getlist('dob[]') or request.form.getlist('dob')
        passports = request.form.getlist('passport_number[]') or request.form.getlist('passport_number')

        # Basic normalization: pad/trim to num_travelers
        def norm(lst):
            lst = list(lst)
            if len(lst) < num_travelers:
                lst += [''] * (num_travelers - len(lst))
            return lst[:num_travelers]

        full_names = norm(full_names)
        genders = norm(genders)
        dobs = norm(dobs)
        passports = norm(passports)

        # Simple validation: require non-empty full_name
        rows = []
        for i in range(num_travelers):
            fn = full_names[i].strip()
            if not fn:
                conn.close()
                flash(f'Traveler {i+1}: Full name is required.')
                return render_template('traveler_details.html', booking_id=booking_id, num_travelers=num_travelers, booking=booking)
            rows.append((booking_id, fn, genders[i] or None, dobs[i] or None, passports[i] or None))

        conn.executemany(
            """
            INSERT INTO traveler_details (booking_id, full_name, gender, dob, passport_number)
            VALUES (?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()
        conn.close()

        flash('Traveler details saved successfully! Proceed to payment.')
        return redirect(url_for('booking.payment', booking_id=booking_id))

    # GET: render a form with num_travelers groups
    conn.close()
    return render_template('traveler_details.html', booking_id=booking_id, num_travelers=num_travelers, booking=booking)

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
