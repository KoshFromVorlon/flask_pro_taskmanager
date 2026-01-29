import pytest
from app import create_app, db
from app.models import User, Task
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Creates the application with an in-memory test database."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,  # Disable CSRF token validation for tests
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
    """Creates initial users for testing."""
    with app.app_context():
        # Create a regular user
        user = User(username='testuser', password=generate_password_hash('password', method='scrypt'))

        # Create a second user (to test access control and isolation)
        user2 = User(username='otheruser', password=generate_password_hash('password', method='scrypt'))

        db.session.add(user)
        db.session.add(user2)
        db.session.commit()

        yield db


@pytest.fixture
def auth_client(client, init_database):
    """A test client that is already logged in as 'testuser'."""
    client.post('/login', data={'username': 'testuser', 'password': 'password'})
    return client