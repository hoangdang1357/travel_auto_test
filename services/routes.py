
from flask import Blueprint, render_template, request
from database import get_db_connection

services_bp = Blueprint('services', __name__,
                        template_folder='../templates/services')

@services_bp.route('/')
def index():
    destination = request.args.get('destination')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_rating = request.args.get('min_rating', type=float)

    query = 'SELECT * FROM travel_services WHERE 1=1'
    params = []

    if destination:
        query += ' AND destination LIKE ?'
        params.append(f'%{destination}%')
    if min_price is not None:
        query += ' AND price >= ?'
        params.append(min_price)
    if max_price is not None:
        query += ' AND price <= ?'
        params.append(max_price)
    if min_rating is not None:
        query += ' AND rating >= ?'
        params.append(min_rating)

    conn = get_db_connection()
    services = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('services/index.html', services=services)

@services_bp.route('/<int:service_id>')
def details(service_id):
    conn = get_db_connection()
    service = conn.execute('SELECT * FROM travel_services WHERE service_id = ?', (service_id,)).fetchone()
    conn.close()
    return render_template('details.html', service=service)
