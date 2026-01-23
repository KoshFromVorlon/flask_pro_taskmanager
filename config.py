import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-dev'
    # Если есть DATABASE_URL (в облаке), берем её, иначе создаем локальный файл
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
