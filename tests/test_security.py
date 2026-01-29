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
        # 'otheruser' is created in conftest.py
        other_user = User.query.filter_by(username='otheruser').first()
        task = Task(content="Secret Task", user_id=other_user.id)

        db = app.extensions['sqlalchemy']
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    # Attempt to delete the task using 'testuser' session (auth_client)
    auth_client.get(f'/delete/{task_id}', follow_redirects=True)

    # Verification: The task should still exist in the database
    with app.app_context():
        assert Task.query.get(task_id) is not None