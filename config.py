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

    # --- SECURITY CONFIGURATION ---
    # Prevents JavaScript from reading session cookies (Defense against XSS)
    SESSION_COOKIE_HTTPONLY = True

    # Restricts cookie sending to first-party context (Defense against CSRF)
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Ensure cookies are only sent over HTTPS (Production only)
    # We check if 'RENDER' env var is set to determine if we are in production
    if os.environ.get('RENDER'):
        SESSION_COOKIE_SECURE = True