from flask import request, jsonify
from marshmallow import ValidationError

from app.extensions import db
from app.auth import token_required
from app.models import Inventory
from . import inventory_bp
from .schemas import inventory_schema, inventory_list_schema


# CREATE INVENTORY ITEM
@inventory_bp.route("/", methods=["POST"])
@token_required  # assume only logged-in users can modify inventory
def create_inventory_item(customer_id):
    json_data = request.get_json() or {}

    try:
        item = inventory_schema.load(json_data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(item)
    db.session.commit()
    return inventory_schema.jsonify(item), 201


# GET ALL INVENTORY
@inventory_bp.route("/", methods=["GET"])
def get_inventory():
    items = Inventory.query.all()
    return inventory_list_schema.jsonify(items), 200


# GET SINGLE INVENTORY ITEM
@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({"error": "Inventory item not found"}), 404
    return inventory_schema.jsonify(item), 200


# UPDATE INVENTORY ITEM
@inventory_bp.route("/<int:item_id>", methods=["PUT"])
@token_required
def update_inventory_item(customer_id, item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({"error": "Inventory item not found"}), 404

    json_data = request.get_json() or {}

    try:
        item = inventory_schema.load(json_data, instance=item, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return inventory_schema.jsonify(item), 200


# DELETE INVENTORY ITEM
@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
@token_required
def delete_inventory_item(customer_id, item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({"error": "Inventory item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f"Inventory item {item_id} deleted"}), 200
