from flask_login import UserMixin
from datetime import datetime, timezone
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)  # Scrypt hash is long
    avatar = db.Column(db.String(150), default='default.png')
    is_admin = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='author', lazy=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default='other')
    # FIX: Use lambda with timezone.utc to avoid DeprecationWarning
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    deadline = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    position = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    subtasks = db.relationship('Subtask', backref='parent_task', lazy=True, cascade="all, delete-orphan")
    attachments = db.relationship('Attachment', backref='parent_task', lazy=True, cascade="all, delete-orphan")

    def get_progress(self):
        total = len(self.subtasks)
        if total == 0: return 0
        completed = sum(1 for sub in self.subtasks if sub.completed)
        return int((completed / total) * 100)


class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)


class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)  # Secure unique name
    original_name = db.Column(db.String(100), nullable=False)  # User's original name
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    allowed_extensions = db.Column(db.String(200),
                                   default="txt,pdf,png,jpg,jpeg,gif,doc,docx,xls,xlsx,ppt,pptx,zip,rar")
    max_file_size_mb = db.Column(db.Integer, default=10)

    @staticmethod
    def get_settings():
        settings = Settings.query.first()
        if not settings:
            settings = Settings()
            db.session.add(settings)
            db.session.commit()
        return settings