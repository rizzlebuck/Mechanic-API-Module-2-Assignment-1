from datetime import datetime

from app.extensions import db


# Many-to-many: Mechanics <-> ServiceTickets
mechanic_service_ticket = db.Table(
    "mechanic_service_ticket",
    db.Column("mechanic_id", db.Integer, db.ForeignKey("mechanics.id"), primary_key=True),
    db.Column(
        "service_ticket_id",
        db.Integer,
        db.ForeignKey("service_tickets.id"),
        primary_key=True,
    ),
)

# Many-to-many: Inventory <-> ServiceTickets (parts per ticket)
ticket_inventory = db.Table(
    "ticket_inventory",
    db.Column("inventory_id", db.Integer, db.ForeignKey("inventory.id"), primary_key=True),
    db.Column(
        "service_ticket_id",
        db.Integer,
        db.ForeignKey("service_tickets.id"),
        primary_key=True,
    ),
)


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # plain for demo only
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    service_tickets = db.relationship(
        "ServiceTicket",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Customer id={self.id} email={self.email!r}>"


class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=mechanic_service_ticket,
        back_populates="mechanics",
    )

    def __repr__(self) -> str:
        return f"<Mechanic id={self.id} name={self.name!r}>"


class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    vehicle = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default="open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    customer = db.relationship("Customer", back_populates="service_tickets")

    mechanics = db.relationship(
        "Mechanic",
        secondary=mechanic_service_ticket,
        back_populates="service_tickets",
    )

    parts = db.relationship(
        "Inventory",
        secondary=ticket_inventory,
        back_populates="tickets",
    )

    def __repr__(self) -> str:
        return f"<ServiceTicket id={self.id} status={self.status!r}>"


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

    tickets = db.relationship(
        "ServiceTicket",
        secondary=ticket_inventory,
        back_populates="parts",
    )

    def __repr__(self) -> str:
        return f"<Inventory id={self.id} name={self.name!r}>"
