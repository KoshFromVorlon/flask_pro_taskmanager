import os


class Config:
    # Секретный ключ берется из окружения или используется дефолтный
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'твоя_очень_секретная_строка'

    # Приоритет 1: Переменная DATABASE_URL (от Docker/Postgres)
    # Приоритет 2: Локальный файл SQLite (для тестов без Docker)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False