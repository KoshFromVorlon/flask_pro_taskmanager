import pytest
from flask import request
from app import db
from app.models import Task, User
from werkzeug.security import generate_password_hash


# --- EXISTING TESTS (Access Control) ---

def test_access_denied_anonymous(client):
    """Anonymous users should not see tasks and must be redirected to login."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_cannot_delete_others_task(auth_client, client, app):
    """User 'testuser' must NOT be able to delete a task belonging to 'otheruser'."""

    with app.app_context():
        # Create 'otheruser' if doesn't exist
        other_user = User.query.filter_by(username='otheruser').first()
        if not other_user:
            other_user = User(username='otheruser')
            other_user.password = generate_password_hash('StrongPass1', method='scrypt')
            db.session.add(other_user)
            db.session.commit()

        task = Task(content="Secret Task", user_id=other_user.id)
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    # Attempt to delete
    auth_client.get(f'/delete/{task_id}', follow_redirects=True)

    # Verification
    with app.app_context():
        assert Task.query.get(task_id) is not None


# --- NEW SECURITY TESTS (FIXED) ---

def test_password_complexity_validator(client, app):
    """Ensure registration rejects weak passwords."""

    # FIX: We use different fake IP addresses for each request (REMOTE_ADDR)
    # to bypass the Rate Limiter without needing to disable it globally.

    # Case A: Password too short (< 8 chars)
    response = client.post('/register', data={
        'username': 'shortpass',
        'password': '123'
    }, follow_redirects=True, environ_base={'REMOTE_ADDR': '127.0.0.10'})
    assert b'Password must be at least 8 chars' in response.data

    # Case B: No digits (letters only)
    response = client.post('/register', data={
        'username': 'lettersOnly',
        'password': 'passwordonly'
    }, follow_redirects=True, environ_base={'REMOTE_ADDR': '127.0.0.11'})
    assert b'Password must be at least 8 chars' in response.data

    # Case C: No letters (digits only)
    response = client.post('/register', data={
        'username': 'digitsOnly',
        'password': '1234567890'
    }, follow_redirects=True, environ_base={'REMOTE_ADDR': '127.0.0.12'})
    assert b'Password must be at least 8 chars' in response.data

    # Case D: Valid strong password
    response = client.post('/register', data={
        'username': 'gooduser',
        'password': 'StrongPass1'
    }, follow_redirects=True, environ_base={'REMOTE_ADDR': '127.0.0.13'})

    # Check for success
    assert b'Password must be at least 8 chars' not in response.data
    assert response.status_code == 200


def test_rate_limiting_login(client, app):
    """
    Test that the login route blocks repeated failed attempts.
    """
    # Create a target user
    with app.app_context():
        if not User.query.filter_by(username='brutetest').first():
            u = User(username='brutetest')
            u.password = generate_password_hash('RealPassword1', method='scrypt')
            db.session.add(u)
            db.session.commit()

    # Attempt 5 logins (the limit is 5 per minute)
    # We use a fixed IP here to intentionally hit the limit
    target_ip = '127.0.0.99'

    for i in range(5):
        response = client.post('/login', data={
            'username': 'brutetest',
            'password': 'WrongPassword'
        }, environ_base={'REMOTE_ADDR': target_ip})

        # Should be 200 (Login page with error) or 302
        assert response.status_code != 429

    # The 6th attempt should trigger the Rate Limiter
    response = client.post('/login', data={
        'username': 'brutetest',
        'password': 'WrongPassword'
    }, environ_base={'REMOTE_ADDR': target_ip})

    assert response.status_code == 429
    assert b'Too Many Requests' in response.data


def test_secure_cookies_headers(client, app):
    """Check that session cookies are set with HttpOnly and SameSite flags."""

    with app.app_context():
        if not User.query.filter_by(username='cookietest').first():
            u = User(username='cookietest')
            u.password = generate_password_hash('CookiePass1', method='scrypt')
            db.session.add(u)
            db.session.commit()

    # Perform a successful login
    response = client.post('/login', data={
        'username': 'cookietest',
        'password': 'CookiePass1'
    }, environ_base={'REMOTE_ADDR': '127.0.0.50'})  # random IP

    cookie_header = response.headers.get('Set-Cookie', '')

    assert 'HttpOnly' in cookie_header
    assert 'SameSite=Lax' in cookie_header