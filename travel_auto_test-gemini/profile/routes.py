
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
from functools import wraps

profile_bp = Blueprint('profile', __name__,
                       template_folder='../templates/profile')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'customer_id' not in session:
            return redirect(url_for('auth.signin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@profile_bp.route('/')
@login_required
def index():
    customer_id = session['customer_id']
    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,)).fetchone()
    conn.close()
    return render_template('profile/index.html', customer=customer)

@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    customer_id = session['customer_id']
    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,)).fetchone()

    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        address = request.form['address']

        conn.execute('UPDATE customers SET full_name = ?, phone = ?, address = ? WHERE customer_id = ?',
                     (full_name, phone, address, customer_id))
        conn.commit()
        conn.close()
        session['customer_name'] = full_name # Update session name
        flash('Profile updated successfully!')
        return redirect(url_for('profile.index'))

    conn.close()
    return render_template('edit_profile.html', customer=customer)

@profile_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        customer_id = session['customer_id']
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        conn = get_db_connection()
        customer = conn.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,)).fetchone()

        if not check_password_hash(customer['password_hash'], current_password):
            flash('Current password is incorrect.')
        else:
            password_hash = generate_password_hash(new_password)
            conn.execute('UPDATE customers SET password_hash = ? WHERE customer_id = ?', (password_hash, customer_id))
            conn.commit()
            flash('Password updated successfully!')
            return redirect(url_for('profile.index'))
        
        conn.close()

    return render_template('change_password.html')
