from app.models import User, Task, Subtask


def test_new_user(init_database):
    """Проверка создания пользователя"""
    user = User.query.filter_by(username='testuser').first()
    assert user.username == 'testuser'
    assert user.password != 'password'  # Пароль должен быть захеширован!


def test_task_progress(app):
    """Проверка логики расчета прогресса задачи"""
    with app.app_context():
        # Создаем задачу
        task = Task(content="Test Task", user_id=1)

        # Добавляем 4 подзадачи
        s1 = Subtask(content="Sub 1", completed=True, parent_task=task)  # Готово
        s2 = Subtask(content="Sub 2", completed=True, parent_task=task)  # Готово
        s3 = Subtask(content="Sub 3", completed=False, parent_task=task)  # Не готово
        s4 = Subtask(content="Sub 4", completed=False, parent_task=task)  # Не готово

        # 2 из 4 готово = 50%
        assert task.get_progress() == 50


def test_empty_subtasks_progress(app):
    """Если подзадач нет, прогресс должен быть 0 (деление на ноль check)"""
    with app.app_context():
        task = Task(content="Empty Task", user_id=1)
        assert task.get_progress() == 0
