from app.models import Task, User
from datetime import datetime


def test_calendar_api(auth_client, app):
    """Проверка, что API отдает правильный JSON для календаря"""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()

        # ИСПРАВЛЕНО: Ставим 2027 год, чтобы задача была в будущем (не просрочена)
        # Если задача просрочена, она становится красной (#dc3545), а мы ждем синюю (#0d6efd)
        task = Task(
            content="Event Task",
            deadline=datetime(2027, 1, 1, 12, 0),
            category='Работа',
            user_id=user.id
        )
        db = app.extensions['sqlalchemy']
        db.session.add(task)
        db.session.commit()

    response = auth_client.get('/api/events')
    assert response.status_code == 200
    data = response.json

    assert len(data) == 1
    assert data[0]['title'] == "Event Task"
    assert "2027-01-01" in data[0]['start']
    # Теперь цвет будет синим, так как дедлайн еще не наступил
    assert data[0]['backgroundColor'] == '#0d6efd'