from app.models import Task, User


def test_update_task(auth_client, app):
    """Тест редактирования текста задачи"""
    # 1. Создаем задачу
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(content="Old Text", user_id=user.id)
        db = app.extensions['sqlalchemy']
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    # 2. Отправляем POST запрос на изменение
    response = auth_client.post(f'/task/{task_id}/update', data={
        'content': 'New Updated Text',
        'category': 'Работа'
    }, follow_redirects=True)

    assert response.status_code == 200

    # 3. Проверяем в базе
    with app.app_context():
        updated_task = Task.query.get(task_id)
        assert updated_task.content == 'New Updated Text'


def test_account_update(auth_client, app):
    """Тест обновления профиля (смена имени)"""
    # ИСПРАВЛЕНО: Маршрут /profile, а не /account
    response = auth_client.post('/profile', data={
        'username': 'new_testuser',
        'picture': (b'', '')
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"new_testuser" in response.data


def test_404_error(client):
    """Тест несуществующей страницы"""
    response = client.get('/non_existent_page')
    assert response.status_code == 404


def test_delete_non_existent_task(auth_client):
    """Попытка удалить задачу, которой нет (должна быть ошибка 404)"""
    response = auth_client.get('/delete/999999')
    assert response.status_code == 404