import pytest
from app import create_app, db
from app.models import User, Task


@pytest.fixture
def app():
    """Создает экземпляр приложения для тестов с временной БД SQLite"""
    app = create_app()

    # ПЕРЕОПРЕДЕЛЯЕМ НАСТРОЙКИ ДЛЯ ТЕСТОВ
    app.config.update({
        "TESTING": True,
        # Используем базу в оперативной памяти (быстро и чисто)
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        # Отключаем защиту CSRF для форм, чтобы упростить тесты
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test_secret_key"
    })

    with app.app_context():
        db.create_all()  # Создаем таблицы
        yield app  # Здесь работают тесты
        db.session.remove()
        db.drop_all()  # Удаляем таблицы после тестов


@pytest.fixture
def client(app):
    """Тестовый клиент (как браузер, но в коде)"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Клиент для тестирования CLI команд"""
    return app.test_cli_runner()


@pytest.fixture
def init_database(app):
    """Создает тестового пользователя"""
    with app.app_context():
        # Создаем пользователя для тестов
        from werkzeug.security import generate_password_hash
        user = User(username='testuser', password=generate_password_hash('password', method='scrypt'))
        db.session.add(user)
        db.session.commit()

        yield db  # Возвращаем управление тесту
