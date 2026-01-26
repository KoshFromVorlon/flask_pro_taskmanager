from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from config import Config
from .translations import translations

db = SQLAlchemy()
login_manager = LoginManager()


# --- НАСТРОЙКИ АДМИНКИ ---
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class UserView(SecureModelView):
    column_list = ('username', 'is_admin', 'tasks')
    form_columns = ('username', 'is_admin')


class TaskView(SecureModelView):
    column_list = ('content', 'category', 'completed', 'author', 'date_created')
    form_columns = ('content', 'category', 'completed', 'author')


# View для Настроек (Запрещаем удалять и создавать новые, можно только редактировать)
class SettingsView(SecureModelView):
    can_create = False
    can_delete = False
    column_list = ('allowed_extensions', 'max_file_size_mb')
    form_columns = ('allowed_extensions', 'max_file_size_mb')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from .models import User, Task, Settings

    admin = Admin(app, name='TaskManager Admin')
    admin.add_view(UserView(User, db.session, name='Пользователи'))
    admin.add_view(TaskView(Task, db.session, name='Задачи'))
    # Добавляем раздел настроек
    admin.add_view(SettingsView(Settings, db.session, name='Настройки сайта'))

    from .routes import main
    app.register_blueprint(main)

    @app.context_processor
    def inject_language():
        lang_code = request.cookies.get('lang', 'ru')
        if lang_code not in translations:
            lang_code = 'ru'
        return dict(lang=lang_code, t=translations[lang_code])

    with app.app_context():
        db.create_all()
        create_default_admin()
        create_default_settings()  # Создаем настройки при запуске

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def create_default_admin():
    from .models import User
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        print("Создание дефолтного админа...")
        hashed_pw = generate_password_hash('admin', method='scrypt')
        admin_user = User(username='admin', password=hashed_pw, is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print("Админ создан: логин 'admin', пароль 'admin'")


def create_default_settings():
    from .models import Settings
    if not Settings.query.first():
        print("Создание настроек по умолчанию...")
        settings = Settings()
        db.session.add(settings)
        db.session.commit()