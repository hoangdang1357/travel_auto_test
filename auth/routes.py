
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
import secrets

from templates.auth.send_email import send_verification_email

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

@auth_bp.route('/verify/<token>')
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


@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        

        conn = get_db_connection()
        customer = conn.execute('SELECT * FROM customers WHERE email = ?', (email,)).fetchone()
        
        if customer:
            verified = customer['verified']
            if not verified:
                flash('Please verify your email before signing in.')
                return redirect(url_for('auth.signin'))

            if check_password_hash(customer['password_hash'], password):
                session['customer_id'] = customer['customer_id']
                session['customer_name'] = customer['full_name']
                flash('Signed in successfully!')
                return redirect(url_for('index'))
        
        flash('Invalid email or password.')
        conn.close()

    return render_template('signin.html')


@auth_bp.route('/logout')
def logout():
    session.pop('customer_id', None)
    session.pop('customer_name', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))
