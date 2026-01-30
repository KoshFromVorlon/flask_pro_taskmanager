from app.models import Task, User
from app import db # Need explicit db import for db.session.get

def test_update_task(auth_client, app):
    """Test editing task content."""
    # 1. Create a task
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(content="Old Text", user_id=user.id)
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    # 2. Send POST request to update
    response = auth_client.post(f'/task/{task_id}/update', data={
        'content': 'New Updated Text',
        'category': 'cat_work'
    }, follow_redirects=True)

    assert response.status_code == 200

    # 3. Verify in database
    with app.app_context():
        # FIX: Use db.session.get() instead of Task.query.get()
        updated_task = db.session.get(Task, task_id)
        assert updated_task.content == 'New Updated Text'
        assert updated_task.category == 'cat_work'


def test_account_update(auth_client, app):
    """Test profile update (username change)."""
    response = auth_client.post('/profile', data={
        'username': 'new_testuser',
        'avatar': (b'', '')  # Simulating empty file upload
    }, follow_redirects=True)

    assert response.status_code == 200
    # Check if the new username appears on the page
    assert b"new_testuser" in response.data


def test_404_error(client):
    """Test accessing a non-existent page."""
    response = client.get('/non_existent_page')
    assert response.status_code == 404


def test_delete_non_existent_task(auth_client):
    """Attempt to delete a task that does not exist (should return 404)."""
    response = auth_client.get('/delete/999999')
    assert response.status_code == 404