from app.models import Task, User


def test_create_task(auth_client, app):
    """Test creating a task via POST request."""
    response = auth_client.post('/', data={
        'content': 'Buy Milk',
        # FIX: Use the category KEY 'cat_home', not the translated word 'Дом'
        'category': 'cat_home',
        'deadline': '2025-12-31T23:59'
    }, follow_redirects=True)

    assert response.status_code == 200
    # Verify the task content appears on the page
    assert b"Buy Milk" in response.data

    with app.app_context():
        assert Task.query.count() == 1
        task = Task.query.first()
        assert task.content == 'Buy Milk'
        # Verify the database stored the key correctly
        assert task.category == 'cat_home'


def test_delete_task(auth_client, app):
    """Test task deletion."""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(content="Delete Me", user_id=user.id)

        db = app.extensions['sqlalchemy']
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = auth_client.get(f'/delete/{task_id}', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        assert Task.query.filter_by(id=task_id).first() is None


def test_toggle_task(auth_client, app):
    """Test toggling task status (completed/uncompleted)."""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(content="Toggle Me", user_id=user.id)

        db = app.extensions['sqlalchemy']
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    # The toggle route returns JSON
    response = auth_client.post(f'/toggle/{task_id}')
    assert response.status_code == 200
    assert response.json['success'] is True
    assert response.json['completed'] is True

    with app.app_context():
        task = Task.query.get(task_id)
        assert task.completed is True