import os
import sqlite3
import unittest
from flask import Flask
from pathlib import Path
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from admin import routes as admin_routes
from services import routes as services_routes

SCHEMA_PATH = PROJECT_ROOT / 'database.sql'


def load_schema(conn):
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()

class TravelServiceComponentTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.NamedTemporaryFile(prefix='tsf_test_', suffix='.sqlite', delete=False)
        tmp.close()
        self.db_path = Path(tmp.name)

        def _test_get_db_connection():
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            conn.execute('PRAGMA foreign_keys = ON;')
            return conn
        import database as database_module
        database_module.get_db_connection = _test_get_db_connection
        admin_routes.get_db_connection = _test_get_db_connection
        services_routes.get_db_connection = _test_get_db_connection

        # bootstrap schema
        conn = _test_get_db_connection(); load_schema(conn); conn.close()

        # seed an admin
        from werkzeug.security import generate_password_hash
        conn = _test_get_db_connection()
        conn.execute("INSERT INTO admins (username, password_hash, email) VALUES (?,?,?)", (
            'admin', generate_password_hash('AdminPass123!'), 'admin@example.com'
        ))
        conn.commit(); conn.close()

        # minimal app with needed blueprints and base template dependencies
        self.app = Flask(__name__, template_folder=str(PROJECT_ROOT / 'templates'))
        self.app.config['SECRET_KEY'] = 'test_secret'
        from flask import Blueprint, session
        # Stub auth blueprint (signin/signup/logout) for base.html links
        auth_bp = Blueprint('auth', __name__)
        @auth_bp.route('/signin')
        def signin():
            return 'AUTH SIGNIN'
        @auth_bp.route('/signup')
        def signup():
            return 'AUTH SIGNUP'
        @auth_bp.route('/logout')
        def logout():
            session.pop('customer_id', None); session.pop('customer_name', None)
            return 'AUTH LOGOUT'

        # Stub profile blueprint
        profile_bp = Blueprint('profile', __name__)
        @profile_bp.route('/')
        def index_profile():
            return 'PROFILE INDEX'

        # Stub booking blueprint (history)
        booking_bp = Blueprint('booking', __name__)
        @booking_bp.route('/history')
        def history():
            return 'BOOKING HISTORY'

        @self.app.before_request
        def ensure_session_keys():
            # Avoid KeyError in base.html
            from flask import session as s
            s.setdefault('customer_name', None)

        self.app.register_blueprint(admin_routes.admin_bp, url_prefix='/admin')
        self.app.register_blueprint(services_routes.services_bp, url_prefix='/services')
        self.app.register_blueprint(auth_bp, url_prefix='')
        self.app.register_blueprint(profile_bp, url_prefix='/profile')
        self.app.register_blueprint(booking_bp, url_prefix='/booking')

        @self.app.route('/')
        def index():
            return 'INDEX'

        self.client = self.app.test_client()
        self._admin_login()

    def tearDown(self):
        if self.db_path.exists():
            try: self.db_path.unlink()
            except OSError: pass

    # helpers
    def _admin_login(self, username='admin', password='AdminPass123!'):
        self.client.post('/admin/login', data={'username': username, 'password': password}, follow_redirects=True)

    def _get_dashboard(self):
        return self.client.get('/admin/dashboard', follow_redirects=True)

    def _extract_services(self):
        conn = sqlite3.connect(self.db_path); conn.row_factory = sqlite3.Row
        rows = conn.execute('SELECT * FROM travel_services ORDER BY service_id').fetchall()
        conn.close(); return rows

    # TSF-01 Add -> View
    def test_tsf_01_add_view_service(self):
        resp = self.client.post('/admin/add_service', data={
            'title': 'Beach Holiday', 'description': 'Desc', 'destination': 'Hawaii', 'price': '1000',
            'rating': '4.8', 'start_date': '2099-01-01', 'end_date': '2099-01-10', 'max_travelers': '20',
            'flight': '', 'hotel': '', 'tour': ''
        }, follow_redirects=True)
        self.assertIn(b'Service added successfully!', resp.data)
        dashboard = self._get_dashboard()
        self.assertIn(b'Beach Holiday', dashboard.data)
        # verify DB
        rows = self._extract_services(); self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['title'], 'Beach Holiday')
        self.assertEqual(int(float(rows[0]['price'])), 1000)

    # TSF-02 Add -> Edit -> View
    def test_tsf_02_add_edit_view_service(self):
        # Add
        self.client.post('/admin/add_service', data={
            'title': 'Winter Tour', 'description': 'Desc', 'destination': 'Alps', 'price': '700',
            'rating': '4.5', 'start_date': '2099-02-01', 'end_date': '2099-02-05', 'max_travelers': '15',
            'flight': '', 'hotel': '', 'tour': ''
        }, follow_redirects=True)
        conn = sqlite3.connect(self.db_path); conn.row_factory = sqlite3.Row
        service_id = conn.execute('SELECT service_id FROM travel_services WHERE title=?', ('Winter Tour',)).fetchone()['service_id']
        conn.close()
        # Edit
        edit_resp = self.client.post(f'/admin/edit_service/{service_id}', data={
            'title': 'Winter Tour Updated', 'description': 'Desc2', 'destination': 'Alps', 'price': '750',
            'rating': '4.7', 'start_date': '2099-02-01', 'end_date': '2099-02-05', 'max_travelers': '15',
            'flight': '', 'hotel': '', 'tour': ''
        }, follow_redirects=True)
        self.assertIn(b'Service updated successfully!', edit_resp.data)
        dashboard = self._get_dashboard()
        self.assertIn(b'Winter Tour Updated', dashboard.data)
        # DB check
        rows = self._extract_services(); self.assertEqual(rows[0]['title'], 'Winter Tour Updated')
        self.assertEqual(int(float(rows[0]['price'])), 750)

    # TSF-03 Add -> Delete -> View
    def test_tsf_03_add_delete_view_service(self):
        add_resp = self.client.post('/admin/add_service', data={
            'title': 'City Break', 'description': 'Desc', 'destination': 'London', 'price': '500',
            'rating': '4.0', 'start_date': '2099-03-01', 'end_date': '2099-03-05', 'max_travelers': '25',
            'flight': '', 'hotel': '', 'tour': ''
        }, follow_redirects=True)
        self.assertIn(b'Service added successfully!', add_resp.data)
        conn = sqlite3.connect(self.db_path); conn.row_factory = sqlite3.Row
        service_id = conn.execute('SELECT service_id FROM travel_services WHERE title=?', ('City Break',)).fetchone()['service_id']
        conn.close()
        del_resp = self.client.post(f'/admin/delete_service/{service_id}', follow_redirects=True)
        self.assertIn(b'Service deleted successfully!', del_resp.data)
        dashboard = self._get_dashboard()
        self.assertNotIn(b'City Break', dashboard.data)

    # TSF-04 Add invalid (empty title) -> ensure not inserted
    def test_tsf_04_add_invalid_service(self):
        # Attempt with empty title; expects validation prevents insertion
        resp = self.client.post('/admin/add_service', data={
            'title': '', 'description': 'Desc', 'destination': 'Nowhere', 'price': '500',
            'rating': '4.0', 'start_date': '2099-04-01', 'end_date': '2099-04-05', 'max_travelers': '10',
            'flight': '', 'hotel': '', 'tour': ''
        }, follow_redirects=True)
        self.assertIn(b'Title is required', resp.data)
        rows = self._extract_services(); self.assertEqual(len(rows), 0)

    # TSF-05 Full CRUD Add -> Edit -> Verify -> Delete -> Verify
    def test_tsf_05_full_crud_flow(self):
        add_resp = self.client.post('/admin/add_service', data={
            'title': 'Flow Package', 'description': 'Desc', 'destination': 'Rome', 'price': '1200',
            'rating': '4.9', 'start_date': '2099-05-01', 'end_date': '2099-05-10', 'max_travelers': '30',
            'flight': '', 'hotel': '', 'tour': ''
        }, follow_redirects=True)
        self.assertIn(b'Service added successfully!', add_resp.data)
        conn = sqlite3.connect(self.db_path); conn.row_factory = sqlite3.Row
        service_id = conn.execute('SELECT service_id FROM travel_services WHERE title=?', ('Flow Package',)).fetchone()['service_id']
        conn.close()
        edit_resp = self.client.post(f'/admin/edit_service/{service_id}', data={
            'title': 'Flow Package Premium', 'description': 'Desc2', 'destination': 'Rome', 'price': '1500',
            'rating': '5.0', 'start_date': '2099-05-01', 'end_date': '2099-05-10', 'max_travelers': '30',
            'flight': '', 'hotel': '', 'tour': ''
        }, follow_redirects=True)
        self.assertIn(b'Service updated successfully!', edit_resp.data)
        dashboard = self._get_dashboard()
        self.assertIn(b'Flow Package Premium', dashboard.data)
        del_resp = self.client.post(f'/admin/delete_service/{service_id}', follow_redirects=True)
        self.assertIn(b'Service deleted successfully!', del_resp.data)
        dashboard2 = self._get_dashboard()
        self.assertNotIn(b'Flow Package Premium', dashboard2.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)
