from app import db
from app.models import Task, User
from werkzeug.security import generate_password_hash

def test_access_denied_anonymous(client):
    """Anonymous users should not see tasks and must be redirected to login."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_cannot_delete_others_task(auth_client, client, app):
    """User 'testuser' must NOT be able to delete a task belonging to 'otheruser'."""
    with app.app_context():
        # Ensure 'otheruser' exists
        other_user = User.query.filter_by(username='otheruser').first()
        if not other_user:
            other_user = User(username='otheruser')
            other_user.password = generate_password_hash('StrongPass1', method='scrypt')
            db.session.add(other_user)
            db.session.commit()

        # Create a task for other_user
        task = Task(content="Secret Task", user_id=other_user.id)
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    # Attempt to delete the task using 'testuser' session (auth_client)
    auth_client.get(f'/delete/{task_id}', follow_redirects=True)

    with app.app_context():
        # FIX: Use db.session.get() instead of Task.query.get() to avoid LegacyAPIWarning
        assert db.session.get(Task, task_id) is not None

def test_home_page_redirect(client):
    """Home page should redirect to Login if not authenticated."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_login_page_loads(client):
    """Login page should load successfully (status 200)."""
    response = client.get('/login')
    assert response.status_code == 200
    # Check for a generic element that exists on the page
    assert b"TaskMaster Pro" in response.data

def test_register_process(client, app):
    """Test new user registration process."""
    client.set_cookie('lang', 'en')

    # FIX: Password must meet complexity requirements (letters + digits)
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'StrongPass1'
    }, follow_redirects=True)

    assert response.status_code == 200

    # Verification: Check if the user was actually created in the DB
    with app.app_context():
        assert User.query.filter_by(username='newuser').first() is not None