from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import func

from app.extensions import db, cache
from app.models import Mechanic, mechanic_service_ticket
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema


# CREATE MECHANIC
@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    json_data = request.get_json() or {}

    try:
        mechanic = mechanic_schema.load(json_data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201


# GET ALL MECHANICS (cached)
@mechanics_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)  # Advanced: caching
def get_mechanics():
    mechanics = Mechanic.query.all()
    return mechanics_schema.jsonify(mechanics), 200


# UPDATE MECHANIC
@mechanics_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id: int):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    json_data = request.get_json() or {}

    try:
        mechanic = mechanic_schema.load(json_data, instance=mechanic, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


# DELETE MECHANIC
@mechanics_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id: int):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted"}), 200


# ADVANCED QUERY: mechanics ordered by number of tickets worked
@mechanics_bp.route("/by-ticket-count", methods=["GET"])
def mechanics_by_ticket_count():
    results = (
        db.session.query(
            Mechanic,
            func.count(mechanic_service_ticket.c.service_ticket_id).label("ticket_count"),
        )
        .outerjoin(
            mechanic_service_ticket,
            Mechanic.id == mechanic_service_ticket.c.mechanic_id,
        )
        .group_by(Mechanic.id)
        .order_by(func.count(mechanic_service_ticket.c.service_ticket_id).desc())
        .all()
    )

    data = [
        {
            "id": mechanic.id,
            "name": mechanic.name,
            "specialization": mechanic.specialization,
            "ticket_count": ticket_count,
        }
        for mechanic, ticket_count in results
    ]
    return jsonify(data), 200
