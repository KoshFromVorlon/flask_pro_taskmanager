from app.models import Task, User
from werkzeug.security import generate_password_hash


def test_access_denied_anonymous(client):
    """Аноним не должен видеть задачи"""
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_cannot_delete_others_task(auth_client, client, app):
    """Пользователь testuser НЕ должен удалить задачу пользователя otheruser"""

    with app.app_context():
        other_user = User.query.filter_by(username='otheruser').first()
        task = Task(content="Secret Task", user_id=other_user.id)
        # ИСПРАВЛЕНО: Убрали .db в конце
        db = app.extensions['sqlalchemy']
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    auth_client.get(f'/delete/{task_id}', follow_redirects=True)

    with app.app_context():
        assert Task.query.get(task_id) is not None