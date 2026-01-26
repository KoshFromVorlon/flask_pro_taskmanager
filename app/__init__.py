from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from config import Config
from .translations import translations  # Импортируем наш словарь

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


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from .models import User, Task

    admin = Admin(app, name='TaskManager Admin')
    admin.add_view(UserView(User, db.session, name='Пользователи'))
    admin.add_view(TaskView(Task, db.session, name='Задачи'))

    from .routes import main
    app.register_blueprint(main)

    # --- МАГИЯ ЯЗЫКОВ ---
    # Эта функция запускается перед отрисовкой любого шаблона
    @app.context_processor
    def inject_language():
        # Получаем язык из куки, по умолчанию 'ru'
        lang_code = request.cookies.get('lang', 'ru')
        # Если в куке мусор, сбрасываем на ru
        if lang_code not in translations:
            lang_code = 'ru'
        # Возвращаем словарь 't', который будет доступен в HTML как {{ t.ключ }}
        return dict(lang=lang_code, t=translations[lang_code])

    with app.app_context():
        db.create_all()
        create_default_admin()

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