import pytest
from app import create_app, db
from app.models import User, Task
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Создает приложение с тестовой БД в памяти"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,  # Отключаем проверку токенов форм для тестов
        "SECRET_KEY": "test_key"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_database(app):
    """Создает двух пользователей: testuser (обычный) и adminuser (админ)"""
    with app.app_context():
        # Обычный юзер
        user = User(username='testuser', password=generate_password_hash('password', method='scrypt'))
        # Второй юзер (для проверки прав доступа)
        user2 = User(username='otheruser', password=generate_password_hash('password', method='scrypt'))

        db.session.add(user)
        db.session.add(user2)
        db.session.commit()

        yield db


@pytest.fixture
def auth_client(client, init_database):
    """Клиент, который уже вошел как 'testuser'"""
    client.post('/login', data={'username': 'testuser', 'password': 'password'})
    return client
