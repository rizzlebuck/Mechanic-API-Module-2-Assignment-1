from flask import Flask

from .extensions import db, ma, limiter, cache
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.inventory import inventory_bp


def create_app(config_name: str = "DevelopmentConfig"):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(f"config.{config_name}")

    # Init extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # Import models so db.create_all() sees them
    from . import models  # noqa: F401 (Telling linter not to warn us)

    # Register blueprints
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    return app
