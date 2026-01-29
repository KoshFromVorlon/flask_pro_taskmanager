from app.models import User, Task, Subtask

def test_new_user(init_database):
    """Test user creation and password hashing."""
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.username == 'testuser'
    assert user.password != 'password'  # Password must be hashed!

def test_task_progress(app):
    """Test task progress calculation logic."""
    with app.app_context():
        # Create a task
        task = Task(content="Test Task", user_id=1)

        # Add 4 subtasks
        s1 = Subtask(content="Sub 1", completed=True, parent_task=task)  # Done
        s2 = Subtask(content="Sub 2", completed=True, parent_task=task)  # Done
        s3 = Subtask(content="Sub 3", completed=False, parent_task=task) # Not done
        s4 = Subtask(content="Sub 4", completed=False, parent_task=task) # Not done

        # 2 out of 4 done = 50%
        assert task.get_progress() == 50

def test_empty_subtasks_progress(app):
    """If there are no subtasks, progress should be 0 (division by zero check)."""
    with app.app_context():
        task = Task(content="Empty Task", user_id=1)
        assert task.get_progress() == 0