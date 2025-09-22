<<<<<<< HEAD
from flask import Blueprint, jsonify, request

services_bp = Blueprint("services", __name__)

# Demo list services
services = [
    {"id": 1, "name": "Ha Long Bay Tour", "destination": "Ha Long", "price": 100},
    {"id": 2, "name": "Sapa Adventure", "destination": "Sapa", "price": 80},
    {"id": 3, "name": "Da Nang Beach", "destination": "Da Nang", "price": 120},
]

@services_bp.route("/", methods=["GET"])
def get_services():
    return jsonify(services), 200

@services_bp.route("/search", methods=["GET"])
def search_services():
    destination = request.args.get("destination")
    max_price = request.args.get("max_price", type=float)

    result = services
    if destination:
        result = [s for s in result if s["destination"].lower() == destination.lower()]
    if max_price is not None:
        result = [s for s in result if s["price"] <= max_price]

    return jsonify(result), 200

@services_bp.route("/<int:service_id>", methods=["GET"])
def service_detail(service_id):
    for s in services:
        if s["id"] == service_id:
            return jsonify(s), 200
    return jsonify({"error": "Service not found"}), 404
=======

from flask import Blueprint, render_template, request, flash
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
        # Validate that max_price > min_price if both provided
        if min_price is not None and max_price <= min_price:
            flash('Max price must be greater than Min price.')
        else:
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
>>>>>>> 1f58bd4957a6ed3a7d95c8be6cb16bb83b883c07
