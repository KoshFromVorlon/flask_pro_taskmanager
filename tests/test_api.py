from app.models import Task, User
from datetime import datetime


def test_calendar_api(auth_client, app):
    """Test that API returns correct JSON for the calendar."""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        db = app.extensions['sqlalchemy']

        # NOTE: We set the year to 2027 to ensure the task is NOT overdue.
        # If a task is overdue, the API forces the color to Red (#dc3545).
        # We want to test the category color (Blue for Work), so the task must be active.
        task = Task(
            content="Event Task",
            deadline=datetime(2027, 1, 1, 12, 0),
            category='cat_work',  # FIX: Use the KEY 'cat_work', not 'Работа'
            user_id=user.id
        )
        db.session.add(task)
        db.session.commit()

    response = auth_client.get('/api/events')
    assert response.status_code == 200
    data = response.json

    assert len(data) == 1
    assert data[0]['title'] == "Event Task"
    assert "2027-01-01" in data[0]['start']

    # Check if the color matches 'cat_work' (#0d6efd)
    assert data[0]['backgroundColor'] == '#0d6efd'