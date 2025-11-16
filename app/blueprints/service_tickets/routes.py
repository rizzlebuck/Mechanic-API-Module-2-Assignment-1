from flask import request, jsonify
from marshmallow import ValidationError

from app.extensions import db
from app.auth import token_required
from app.models import ServiceTicket, Mechanic, Inventory
from . import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema


# CREATE SERVICE TICKET (requires logged-in customer)
@service_tickets_bp.route("/", methods=["POST"])
@token_required
def create_ticket(customer_id):
    json_data = request.get_json() or {}

    try:
        description = json_data["description"]
    except KeyError:
        return jsonify({"error": "description is required"}), 400

    vehicle = json_data.get("vehicle")
    status = json_data.get("status", "open")

    ticket = ServiceTicket(
        description=description,
        vehicle=vehicle,
        status=status,
        customer_id=customer_id,
    )
    db.session.add(ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 201


# GET ALL TICKETS (could be admin-only in real life)
@service_tickets_bp.route("/", methods=["GET"])
def get_tickets():
    tickets = ServiceTicket.query.all()
    return service_tickets_schema.jsonify(tickets), 200


# ADVANCED UPDATE: EDIT MECHANICS ON A TICKET
# PUT '/<int:ticket_id>/edit' : Takes in remove_ids, and add_ids
@service_tickets_bp.route("/<int:ticket_id>/edit", methods=["PUT"])
@token_required  # requires customer to be logged in
def edit_ticket_mechanics(customer_id, ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    # (Optionally: check ownership)
    if ticket.customer_id != customer_id:
        return jsonify({"error": "Not authorized to modify this ticket"}), 403

    json_data = request.get_json() or {}
    add_ids = json_data.get("add_ids", [])
    remove_ids = json_data.get("remove_ids", [])

    # Remove mechanics
    if remove_ids:
        for mid in remove_ids:
            mech = Mechanic.query.get(mid)
            if mech and mech in ticket.mechanics:
                ticket.mechanics.remove(mech)

    # Add mechanics
    if add_ids:
        for mid in add_ids:
            mech = Mechanic.query.get(mid)
            if mech and mech not in ticket.mechanics:
                ticket.mechanics.append(mech)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


# ADD A PART TO A TICKET (Inventory relationship)
@service_tickets_bp.route("/<int:ticket_id>/add-part/<int:inventory_id>", methods=["PUT"])
@token_required
def add_part_to_ticket(customer_id, ticket_id, inventory_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    if ticket.customer_id != customer_id:
        return jsonify({"error": "Not authorized to modify this ticket"}), 403

    part = db.session.get(Inventory, inventory_id)
    if not part:
        return jsonify({"error": "Inventory item not found"}), 404

    if part not in ticket.parts:
        ticket.parts.append(part)
        db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200
