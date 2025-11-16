from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select

from app.extensions import db, limiter
from app.auth import encode_token, token_required
from app.models import Customer, ServiceTicket
from . import customers_bp
from .schemas import customer_schema, customers_schema, login_schema
from app.blueprints.service_tickets.schemas import service_tickets_schema


# CREATE CUSTOMER
@customers_bp.route("/", methods=["POST"])
def create_customer():
    try:
        data = request.get_json() or {}
        # For simplicity, this uses raw dict; you could also use customer_schema.load
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        if not all([name, email, password]):
            return jsonify({"error": "name, email, and password are required"}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    existing = Customer.query.filter_by(email=email).first()
    if existing:
        return jsonify({"error": "Email already registered"}), 400

    customer = Customer(name=name, email=email, password=password)
    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer), 201


# GET CUSTOMERS (with pagination)
@customers_bp.route("/", methods=["GET"])
def get_customers():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 5))
    except ValueError:
        return jsonify({"error": "page and per_page must be integers"}), 400

    pagination = Customer.query.paginate(page=page, per_page=per_page, error_out=False)
    result = {
        "items": customers_schema.dump(pagination.items),
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
    }
    return jsonify(result), 200


# LOGIN (rate limited)
@customers_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")  # Advanced: rate limiting for login attempts
def login():
    json_data = request.get_json() or {}

    try:
        data = login_schema.load(json_data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    email = data["email"]
    password = data["password"]

    customer = Customer.query.filter_by(email=email).first()
    if not customer or customer.password != password:
        return jsonify({"error": "Invalid email or password"}), 401
 
    token = encode_token(customer.id)

    response = {
        "status": "success",
        "message": "successfully logged in.",
        "token": token
    }

    return jsonify(response), 200


# AUTH-PROTECTED: GET MY TICKETS
@customers_bp.route("/my-tickets", methods=["GET"])
@token_required
def my_tickets(customer_id):
    query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200
