class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "super-saiyan-secret"  # Secret key
    JWT_ALGORITHM = "HS256" # For Hashing
    JWT_EXPIRE_MINUTES = 60

    # Flask-Limiter default rate limit (blanket protection)
    RATELIMIT_DEFAULT = "100 per hour"

    # Flask-Caching
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # Simple SQLite DB 
    SQLALCHEMY_DATABASE_URI = "sqlite:///mechanic_shop_advanced.db"


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///mechanic_shop_prod.db"
