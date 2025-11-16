from datetime import datetime, timedelta
from functools import wraps

from flask import request, jsonify, current_app
from jose import jwt, JWTError

from .models import Customer


def encode_token(customer_id: int) -> str:
    """
    Encode a JWT token specific to a customer_id.
    """
    secret = current_app.config["SECRET_KEY"]
    algorithm = current_app.config.get("JWT_ALGORITHM", "HS256")
    minutes = current_app.config.get("JWT_EXPIRE_MINUTES", 60)

    payload = {
        "sub": "customer",
        "customer_id": customer_id,
        "exp": datetime.utcnow() + timedelta(minutes=minutes),
    }

    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token


def token_required(f):
    """
    Decorator that validates Bearer token and injects customer_id
    into the route function: def my_route(customer_id, ...).
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        token = auth_header.split(" ", 1)[1]
        secret = current_app.config["SECRET_KEY"]
        algorithm = current_app.config.get("JWT_ALGORITHM", "HS256")

        try:
            payload = jwt.decode(token, secret, algorithms=[algorithm])
            customer_id = payload.get("customer_id")
            if not customer_id:
                return jsonify({"error": "Token missing customer_id"}), 401
        except JWTError:
            return jsonify({"error": "Invalid or expired token"}), 401

        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        return f(customer_id=customer_id, *args, **kwargs)

    return decorated
