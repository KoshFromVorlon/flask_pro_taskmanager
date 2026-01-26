from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()


# Настройка Админки: кто может заходить
class MyAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    # Какие поля показывать в таблице и форме
    column_list = ('username', 'is_admin', 'tasks')
    form_columns = ('username', 'is_admin')  # Пароль через админку менять не дадим (сложно с хешем), только права


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from .models import User, Task

    # Инициализация админ-панели
    admin = Admin(app, name='TaskManager Admin')
    admin.add_view(MyAdminView(User, db.session))
    admin.add_view(MyAdminView(Task, db.session))

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        create_default_admin()  # <-- ВЫЗОВ ФУНКЦИИ СОЗДАНИЯ АДМИНА

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


# Функция создания дефолтного админа
def create_default_admin():
    from .models import User
    # Проверяем, существует ли пользователь 'admin'
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        # Создаем, если нет
        print("Создание дефолтного админа...")
        hashed_pw = generate_password_hash('admin', method='scrypt')
        admin_user = User(username='admin', password=hashed_pw, is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print("Админ создан: логин 'admin', пароль 'admin'")