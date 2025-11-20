import os
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key is now read from environment, with a safe fallback
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-saiyan-secret"

    # JWT settings (you can also move these into env if you want)
    JWT_ALGORITHM = "HS256"  # For hashing
    JWT_EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE_MINUTES", 60))

    # Flask-Limiter default rate limit (blanket protection)
    RATELIMIT_DEFAULT = os.environ.get("RATELIMIT_DEFAULT", "100 per hour")

    # Flask-Caching
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # Simple SQLite DB (can be overridden via env if you want)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URI",
        "sqlite:///mechanic_shop_advanced.db"
    )


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URI",
        "sqlite:///testing.db"
    )


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

