from app.extensions import ma
from app.models import Inventory


class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True


inventory_schema = InventorySchema()
inventory_list_schema = InventorySchema(many=True)
