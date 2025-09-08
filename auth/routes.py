
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

auth_bp = Blueprint('auth', __name__,
                    template_folder='../templates/auth')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']

        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO customers (full_name, email, password_hash, phone, address) VALUES (?, ?, ?, ?, ?)',
                         (full_name, email, password_hash, phone, address))
            conn.commit()
            flash('Account created successfully! Please sign in.')
            return redirect(url_for('auth.signin'))
        except sqlite3.IntegrityError:
            flash('Email already exists.')
        finally:
            conn.close()

    return render_template('signup.html')

@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        customer = conn.execute('SELECT * FROM customers WHERE email = ?', (email,)).fetchone()
        conn.close()

        if customer and check_password_hash(customer['password_hash'], password):
            session['customer_id'] = customer['customer_id']
            session['customer_name'] = customer['full_name']
            flash('Signed in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')

    return render_template('signin.html')

@auth_bp.route('/logout')
def logout():
    session.pop('customer_id', None)
    session.pop('customer_name', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))
