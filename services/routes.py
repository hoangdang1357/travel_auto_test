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
