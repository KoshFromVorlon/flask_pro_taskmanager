from app.models import Task, User

def test_access_denied_anonymous(client):
    """Anonymous users should not see tasks and must be redirected to login."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_cannot_delete_others_task(auth_client, client, app):
    """User 'testuser' must NOT be able to delete a task belonging to 'otheruser'."""
    with app.app_context():
        other_user = User.query.filter_by(username='otheruser').first()
        task = Task(content="Secret Task", user_id=other_user.id)
        db = app.extensions['sqlalchemy']
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    auth_client.get(f'/delete/{task_id}', follow_redirects=True)

    with app.app_context():
        assert Task.query.get(task_id) is not None

def test_home_page_redirect(client):
    """Home page should redirect to Login if not authenticated."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_login_page_loads(client):
    """Login page should load successfully (status 200)."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"TaskMaster Pro" in response.data

def test_register_process(client, app):
    """Test new user registration process."""
    client.set_cookie('lang', 'en')

    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Registration successful! Welcome." in response.data

    with app.app_context():
        from app.models import User
        assert User.query.filter_by(username='newuser').first() is not None