from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
import secrets

from templates.auth.send_email import send_verification_email
import os
from flask import jsonify

auth_bp = Blueprint('auth', __name__,
                    template_folder='../templates/auth')


def generate_verification_code():
    return secrets.token_urlsafe(16)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']
        token = generate_verification_code()
        

        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO customers (full_name, email, password_hash, phone, address, verification_code) VALUES (?, ?, ?, ?, ?, ?)',
                         (full_name, email, password_hash, phone, address, token))
            conn.commit()
            send_verification_email(email, token=token)
            flash('Account created successfully! Please check your email to verify your account.')
            return redirect(url_for('auth.signin'))
        except sqlite3.IntegrityError:
            flash('Email already exists.')
        finally:
            conn.close()

    return render_template('signup.html')

@auth_bp.route('/signup/<token>', methods=['GET'])
def verify_email(token):
    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM customers WHERE verification_code = ?', (token,)).fetchone()
    if customer:
        conn.execute('UPDATE customers SET verified = 1, verification_code = NULL WHERE customer_id = ?', (customer['customer_id'],))
        conn.commit()
        flash('Email verified successfully! You can now sign in.')
    else:
        flash('Invalid or expired verification link.')
    conn.close()
    return redirect(url_for('auth.signin'))

def validate_login_credentials(email, password):
    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM customers WHERE email = ?', (email,)).fetchone()
    verified = customer['verified'] if customer else 0
    conn.close()
    
    if not verified:
        return False, 'Please verify your email before signing in.'

    if customer and check_password_hash(customer['password_hash'], password):
        return True, customer
    else:
        return False, 'Invalid email or password.'

@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Use the reusable function
        is_valid, result = validate_login_credentials(email, password)

        if is_valid:
            customer = result
            session['customer_id'] = customer['customer_id']
            session['customer_name'] = customer['full_name']
            flash('Signed in successfully!')
            return redirect(url_for('index'))
        else:
            flash(result)  # result contains the error message

    return render_template('signin.html')


@auth_bp.route('/logout')
def logout():
    session.pop('customer_id', None)
    session.pop('customer_name', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'customer_id' not in session:
        flash('Please sign in first.')
        return redirect(url_for('auth.signin'))
    customer_id = session['customer_id']
    conn = get_db_connection()
    customer = conn.execute('SELECT customer_id, full_name, email, phone, address FROM customers WHERE customer_id=?',
                            (customer_id,)).fetchone()
    if not customer:
        conn.close()
        flash('Account not found.')
        return redirect(url_for('auth.signin'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip() or None
        address = request.form.get('address', '').strip()
        try:
            conn.execute('UPDATE customers SET full_name=?, email=?, phone=?, address=? WHERE customer_id=?',
                         (full_name, email, phone, address, customer_id))
            conn.commit()
            session['customer_name'] = full_name
            flash('Profile updated successfully.')
            # Refresh customer
            customer = conn.execute('SELECT customer_id, full_name, email, phone, address FROM customers WHERE customer_id=?',
                                    (customer_id,)).fetchone()
        except sqlite3.IntegrityError:
            flash('Email already exists.')
        except sqlite3.DatabaseError as e:
            # Likely trigger violation (e.g., invalid phone)
            msg = str(e)
            if 'Invalid phone' in msg:
                flash('Invalid phone: must be 10 digits starting with 0')
            else:
                flash('Failed to update profile.')
        finally:
            conn.close()
        return redirect(url_for('auth.profile'))
    conn.close()
    # Minimal inline rendering (tests only rely on flashes, not template)
    return render_template('profile.html', customer=customer)

# Test-only endpoint: retrieve verification token for an email
# This is intended for automated tests only and requires a secret key set in
# the server environment variable TEST_ENDPOINT_KEY. It returns JSON {"token": "..."}
# when the key matches; otherwise it returns 403 or empty.
@auth_bp.route('/_test/get_verification_token', methods=['POST'])
def _test_get_verification_token():
    try:
        data = request.get_json(force=True)
        email = data.get('email')
        key = data.get('key')
    except Exception:
        return jsonify({'error': 'invalid request'}), 400

    secret = os.getenv('TEST_ENDPOINT_KEY', '')
    if not secret or key != secret:
        return jsonify({'error': 'forbidden'}), 403

    conn = get_db_connection()
    row = conn.execute('SELECT verification_code FROM customers WHERE email = ? ORDER BY customer_id DESC LIMIT 1', (email,)).fetchone()
    conn.close()
    if not row or not row['verification_code']:
        return jsonify({'token': None}), 200
    return jsonify({'token': row['verification_code']}), 200
