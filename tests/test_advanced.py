import pytest
from app.models import User, Task, Subtask, Attachment
from app import db
from datetime import datetime


# --- ADVANCED TASK EDITING TESTS ---

def test_get_task_details_json(auth_client, app):
    """
    Test the API endpoint that provides full task data for the edit modal.
    Verifies that JSON contains content, category, and subtasks.
    """
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(content="Modal Task", category='cat_work', user_id=user.id)
        sub = Subtask(content="SubItem", parent_task=task)

        db.session.add(task)
        db.session.add(sub)
        db.session.commit()
        task_id = task.id

    # Fetch task details via JSON API
    response = auth_client.get(f'/task/{task_id}/details')

    assert response.status_code == 200
    data = response.json
    assert data['content'] == "Modal Task"
    assert data['category'] == "cat_work"
    assert len(data['subtasks']) == 1
    assert data['subtasks'][0]['content'] == "SubItem"


def test_full_update_task_functionality(auth_client, app):
    """
    Test the full update route (content, category, description, deadline).
    Ensures that changes are correctly persisted in the database.
    """
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        # Create a task with original values
        task = Task(content="Original Title", description="Old Desc", user_id=user.id)

        db.session.add(task)
        db.session.commit()
        task_id = task.id

    # Submit the full update form data
    response = auth_client.post(f'/task/{task_id}/full_update', data={
        'content': 'Updated Title',
        'category': 'cat_study',
        'description': 'New Description',
        'deadline': '2026-05-20T15:00'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['success'] is True

    # Verify updates in the database
    with app.app_context():
        # FIX: Use db.session.get() instead of Task.query.get()
        updated_task = db.session.get(Task, task_id)
        assert updated_task.content == 'Updated Title'
        assert updated_task.category == 'cat_study'
        assert updated_task.description == 'New Description'
        assert updated_task.deadline.year == 2026


def test_subtask_content_editing(auth_client, app):
    """
    Test updating the text content of an existing subtask.
    Verifies that the subtask content changes without affecting other fields.
    """
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(content="Parent", user_id=user.id)
        sub = Subtask(content="Old Subtask", parent_task=task)
        db.session.add(task)
        db.session.add(sub)
        db.session.commit()
        sub_id = sub.id

    # Submit new content as JSON
    response = auth_client.post(f'/subtask/{sub_id}/update_text', json={
        'content': 'New Subtask Text'
    })

    assert response.status_code == 200
    assert response.json['success'] is True

    # Check DB for the updated subtask text
    with app.app_context():
        # FIX: Use db.session.get()
        updated_sub = db.session.get(Subtask, sub_id)
        assert updated_sub.content == 'New Subtask Text'


def test_attachment_database_deletion(auth_client, app):
    """
    Test removing an attachment record from the database.
    Ensures the link between the task and the file is severed.
    """
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(content="File Task", user_id=user.id)
        # Simulate an existing attachment
        attachment = Attachment(
            filename="secure_name.txt",
            original_name="my_doc.txt",
            parent_task=task
        )
        db.session.add(task)
        db.session.add(attachment)
        db.session.commit()
        att_id = attachment.id

    # Perform deletion via POST request
    response = auth_client.post(f'/attachment/{att_id}/delete')

    assert response.status_code == 200
    assert response.json['success'] is True

    # Ensure the attachment is gone from the database
    with app.app_context():
        # FIX: Use db.session.get()
        assert db.session.get(Attachment, att_id) is None