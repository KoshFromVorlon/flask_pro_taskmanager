from app.models import Task, User


def test_create_task(auth_client, app):
    """Тест создания задачи через POST-запрос"""
    response = auth_client.post('/', data={
        'content': 'Buy Milk',
        'category': 'Дом',
        'deadline': '2025-12-31T23:59'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Buy Milk" in response.data

    with app.app_context():
        assert Task.query.count() == 1
        task = Task.query.first()
        assert task.content == 'Buy Milk'
        assert task.category == 'Дом'


def test_delete_task(auth_client, app):
    """Тест удаления задачи"""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(content="Delete Me", user_id=user.id)
        # ИСПРАВЛЕНО: Убрали .db в конце
        db = app.extensions['sqlalchemy']
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = auth_client.get(f'/delete/{task_id}', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        assert Task.query.filter_by(id=task_id).first() is None


def test_toggle_task(auth_client, app):
    """Тест переключения статуса"""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(content="Toggle Me", user_id=user.id)
        # ИСПРАВЛЕНО: Убрали .db в конце
        db = app.extensions['sqlalchemy']
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = auth_client.post(f'/toggle/{task_id}')
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['completed'] == True

    with app.app_context():
        task = Task.query.get(task_id)
        assert task.completed is True