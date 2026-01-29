def test_home_page_redirect(client):
    """Home page should redirect to Login if not authenticated."""
    response = client.get('/')
    assert response.status_code == 302  # 302 Found (Redirect)
    assert '/login' in response.headers['Location']


def test_login_page_loads(client):
    """Login page should load successfully (status 200)."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"TaskMaster Pro" in response.data  # Check if site title is present


def test_register_process(client, app):
    """Test new user registration process."""
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpassword'
    }, follow_redirects=True)

    # After registration, it should redirect to index and show a flash message
    assert response.status_code == 200

    # UPDATE: We now check for the ENGLISH success message
    # Key: 'flash_register_success' -> 'Registration successful! Welcome.'
    assert b"Registration successful! Welcome." in response.data

    with app.app_context():
        from app.models import User
        assert User.query.filter_by(username='newuser').first() is not None