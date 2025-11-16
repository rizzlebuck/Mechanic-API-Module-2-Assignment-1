# app/blueprints/customers/schemas.py

from app.extensions import ma
from app.models import Customer


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        # Don't expose password when serializing customers
        exclude = ("password",)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


class LoginSchema(ma.Schema):
    email = ma.Email(required=True)
    password = ma.String(required=True)


login_schema = LoginSchema()
