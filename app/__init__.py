from flask import Flask

from dotenv import load_dotenv
import os

from .extensions import db, ma, limiter, cache
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.inventory import inventory_bp

from flask_swagger_ui import get_swaggerui_blueprint

# Swagger UI config
SWAGGER_URL = "/api/docs"          # URL where Swagger UI will be served
API_URL = "/static/swagger.yaml"   # Path to swagger.yaml 

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Mechanic Shop Advanced API"
    },
)


def create_app(config_name: str = "DevelopmentConfig"):
    load_dotenv()   # <-- loads .env into environment variables
    
    """
    Application Factory.
    Creates and configures an instance of the Flask app.
    """
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object(f"config.{config_name}")

    # Initialize extensions with this app
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # Import models so db.create_all() sees them
    from . import models  # noqa: F401

    # Register blueprints for API resources
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    # Register Swagger UI blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
