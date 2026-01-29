import os

class Config:
    # Secret key is loaded from the environment or defaults to a hardcoded string
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-very-secret-string'

    # Database Configuration:
    # Priority 1: DATABASE_URL environment variable (from Docker/Render/Postgres)
    # Priority 2: Local SQLite file (for local development/testing)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'

    # Fix for Render: SQLAlchemy requires 'postgresql://', but Render provides 'postgres://'
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False