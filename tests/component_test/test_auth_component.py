import os
import sqlite3
import unittest
from flask import Flask
from pathlib import Path
import sys

# Ensure project root is on sys.path before importing routes.py
# (Now two levels up because file moved into component_test/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from auth import routes as auth_routes  # import routes.py explicitly

BASE_DIR = PROJECT_ROOT
SCHEMA_PATH = BASE_DIR / 'database.sql'


def load_schema(conn):
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()


class AuthTestSuite(unittest.TestCase):
    def setUp(self):
        # One temp DB reused per test (fresh each time)
        self.db_path = BASE_DIR / 'test_auth.sqlite'
        if self.db_path.exists():
            self.db_path.unlink()

        def _test_get_db_connection():
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        auth_routes.get_db_connection = _test_get_db_connection
        auth_routes.send_verification_email = lambda email, token: None

        conn = auth_routes.get_db_connection()
        load_schema(conn)
        conn.close()

        # Create test app with correct template folder so extending base.html works
        self.app = Flask(__name__, template_folder=str(BASE_DIR / 'templates'))
        self.app.config['SECRET_KEY'] = 'test_secret'
        # Provide minimal stub routes/blueprints required by base.html
        @self.app.route('/')
        def index():  # pragma: no cover - trivial helper
            return 'INDEX'

        # Stub services blueprint endpoint used in base.html
        from flask import Blueprint
        services_bp = Blueprint('services', __name__)
        @services_bp.route('/')
        def index():  # pragma: no cover
            return 'SERVICES'
        self.app.register_blueprint(services_bp, url_prefix='/services')

        # Stub profile blueprint index used in base.html conditional
        profile_bp = Blueprint('profile', __name__)
        @profile_bp.route('/')
        def index_profile():  # endpoint name profile.index
            return 'PROFILE'
        self.app.register_blueprint(profile_bp, url_prefix='/profile')

        # Stub booking blueprint history endpoint
        booking_bp = Blueprint('booking', __name__)
        @booking_bp.route('/history')
        def history():  # endpoint booking.history
            return 'HISTORY'
        self.app.register_blueprint(booking_bp, url_prefix='/booking')

        # Stub admin blueprint login endpoint
        admin_bp = Blueprint('admin', __name__)
        @admin_bp.route('/login')
        def login():  # endpoint admin.login
            return 'ADMIN LOGIN'
        self.app.register_blueprint(admin_bp, url_prefix='/admin')

        self.app.register_blueprint(auth_routes.auth_bp)
        self.client = self.app.test_client()
        os.environ['TEST_ENDPOINT_KEY'] = 'TEST_KEY_123'

    def tearDown(self):
        if self.db_path.exists():
            self.db_path.unlink()

    # Helpers (giữ tên cũ để test hiện có không đổi)
    def _signup(self, email='user@example.com', password='Password123!', full_name='Test User',
                phone='0123456789', address='123 Test St'):
        return self.client.post('/signup', data={
            'full_name': full_name,
            'email': email,
            'password': password,
            'phone': phone,
            'address': address
        }, follow_redirects=True)

    def _get_verification_code(self, email):
        conn = auth_routes.get_db_connection()
        row = conn.execute('SELECT verification_code FROM customers WHERE email=?', (email,)).fetchone()
        conn.close()
        return row['verification_code'] if row else None

    # Flow helper aliases
    def signup(self, *a, **kw): return self._signup(*a, **kw)
    def get_token(self, email): return self._get_verification_code(email)
    def verify(self, token): return self.client.get(f'/signup/{token}', follow_redirects=True)
    def signin(self, email, password):
        return self.client.post('/signin', data={'email': email, 'password': password}, follow_redirects=True)
    def update_profile(self, full_name='Updated Flow', email='flow1@example.com',
                       phone='0123456789', address='New Addr'):
        return self.client.post('/profile', data={
            'full_name': full_name, 'email': email, 'phone': phone, 'address': address
        }, follow_redirects=True)

    # Flow tests
    def test_flow_01_full_success_register_verify_login_update(self):
        self.signup(email='flow1@example.com')
        token = self.get_token('flow1@example.com')
        self.assertTrue(token)
        self.verify(token)
        r_login = self.signin('flow1@example.com', 'Password123!')
        self.assertIn(b'Signed in successfully', r_login.data)
        r_update = self.update_profile(full_name='Flow Updated', email='flow1@example.com', address='Addr 2')
        self.assertIn(b'Profile updated successfully', r_update.data)

    def test_flow_02_register_duplicate_email(self):
        self.signup(email='flow1@example.com')
        r2 = self.signup(email='flow1@example.com')
        self.assertIn(b'Email already exists', r2.data)

    def test_flow_03_login_wrong_password(self):
        self.signup(email='flow1@example.com')
        token = self.get_token('flow1@example.com')
        self.verify(token)
        r_login = self.signin('flow1@example.com', 'WrongPass!')
        self.assertIn(b'Invalid email or password', r_login.data)

    def test_flow_04_update_requires_login(self):
        r = self.client.post('/profile', data={
            'full_name': 'X', 'email': 'x@example.com'
        }, follow_redirects=True)
        self.assertIn(b'Please sign in first', r.data)

    def test_flow_05_update_invalid_phone(self):
        self.signup(email='flow1@example.com')
        token = self.get_token('flow1@example.com')
        self.verify(token)
        self.signin('flow1@example.com', 'Password123!')
        r = self.update_profile(email='flow1@example.com', phone='123')
        self.assertIn(b'Invalid phone', r.data)

    def test_flow_06_update_duplicate_email(self):
        self.signup(email='flow1@example.com')
        token1 = self.get_token('flow1@example.com')
        self.verify(token1)
        self.signup(email='flow2@example.com')
        token2 = self.get_token('flow2@example.com')
        self.verify(token2)
        self.signin('flow1@example.com', 'Password123!')
        r = self.update_profile(email='flow2@example.com')
        self.assertIn(b'Email already exists', r.data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
