from . import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    avatar = db.Column(db.String(150), nullable=False, default='default.png')
    is_admin = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='author', lazy=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='Другое')
    deadline = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    subtasks = db.relationship('Subtask', backref='parent_task', lazy=True, cascade="all, delete-orphan")
    attachments = db.relationship('Attachment', backref='parent_task', lazy=True, cascade="all, delete-orphan")

    def get_progress(self):
        total = len(self.subtasks)
        if total == 0:
            return 0
        done = sum(1 for s in self.subtasks if s.completed)
        return int((done / total) * 100)


class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)


class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    original_name = db.Column(db.String(150), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)