from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()


# Защита админки: пускаем только админов
class MyAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from .models import User, Task

    # Регистрация админки
    admin = Admin(app, name='TaskManager Admin')
    admin.add_view(MyAdminView(User, db.session))
    admin.add_view(MyAdminView(Task, db.session))

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()  # Создаем таблицы при запуске

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
