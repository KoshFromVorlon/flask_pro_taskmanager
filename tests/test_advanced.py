from app.models import Task, Subtask, Attachment, User
from datetime import datetime


def test_get_task_details(auth_client, app):
    """Тест API для получения данных задачи в модальное окно (JSON)."""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(content="Modal Task", category='cat_work', user_id=user.id)
        # Добавим подзадачу сразу
        sub = Subtask(content="SubItem", parent_task=task)

        db = app.extensions['sqlalchemy']
        db.session.add(task)
        db.session.add(sub)
        db.session.commit()
        task_id = task.id

    # Запрашиваем данные для модалки
    response = auth_client.get(f'/task/{task_id}/details')

    assert response.status_code == 200
    data = response.json

    # Проверяем, что вернулись правильные поля
    assert data['content'] == "Modal Task"
    assert data['category'] == "cat_work"
    assert len(data['subtasks']) == 1
    assert data['subtasks'][0]['content'] == "SubItem"


def test_full_update_task(auth_client, app):
    """Тест полного редактирования задачи (название, описание, категория)."""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(content="Original Title", description="Old Desc", user_id=user.id)

        db = app.extensions['sqlalchemy']
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    # Отправляем форму полного обновления
    response = auth_client.post(f'/task/{task_id}/full_update', data={
        'content': 'Updated Title',
        'category': 'cat_study',
        'description': 'New Description',
        'deadline': '2026-05-20T15:00'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['success'] is True

    # Проверяем базу
    with app.app_context():
        updated_task = Task.query.get(task_id)
        assert updated_task.content == 'Updated Title'
        assert updated_task.category == 'cat_study'
        assert updated_task.description == 'New Description'
        assert updated_task.deadline.year == 2026


def test_update_subtask_text(auth_client, app):
    """Тест редактирования текста подзадачи."""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(content="Parent", user_id=user.id)
        sub = Subtask(content="Old Subtask", parent_task=task)

        db = app.extensions['sqlalchemy']
        db.session.add(task)
        db.session.add(sub)
        db.session.commit()
        sub_id = sub.id

    # Отправляем JSON с новым текстом
    response = auth_client.post(f'/subtask/{sub_id}/update_text', json={
        'content': 'New Subtask Text'
    })

    assert response.status_code == 200
    assert response.json['success'] is True

    # Проверяем базу
    with app.app_context():
        updated_sub = Subtask.query.get(sub_id)
        assert updated_sub.content == 'New Subtask Text'


def test_delete_attachment_db(auth_client, app):
    """Тест удаления записи о файле из базы данных."""
    # Примечание: Мы не тестируем физическое удаление с диска, так как в тестах
    # сложно мокать файловую систему без доп. библиотек, но проверяем логику БД.

    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(content="File Task", user_id=user.id)
        # Имитируем прикрепленный файл
        attachment = Attachment(
            filename="secure_name.txt",
            original_name="my_doc.txt",
            parent_task=task
        )

        db = app.extensions['sqlalchemy']
        db.session.add(task)
        db.session.add(attachment)
        db.session.commit()
        att_id = attachment.id

    # Удаляем файл
    response = auth_client.post(f'/attachment/{att_id}/delete')

    assert response.status_code == 200
    assert response.json['success'] is True

    # Проверяем, что файл исчез из базы
    with app.app_context():
        assert Attachment.query.get(att_id) is None
