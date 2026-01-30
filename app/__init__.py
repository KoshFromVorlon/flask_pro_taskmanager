from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from .translations import translations

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Initialize Limiter for brute-force protection
# We use in-memory storage, which is sufficient for this deployment
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# --- ADMIN PANEL CONFIGURATION ---
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class UserView(SecureModelView):
    column_list = ('username', 'is_admin', 'tasks')
    form_columns = ('username', 'is_admin')

class TaskView(SecureModelView):
    column_list = ('content', 'category', 'completed', 'author', 'date_created')
    form_columns = ('content', 'category', 'completed', 'author')

class SettingsView(SecureModelView):
    can_create = False
    can_delete = False
    column_list = ('allowed_extensions', 'max_file_size_mb')
    form_columns = ('allowed_extensions', 'max_file_size_mb')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # Initialize Migration engine
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Initialize Rate Limiter
    limiter.init_app(app)

    from .models import User, Task, Settings

    # Initialize Admin Panel
    # 'template_mode="bootstrap4"' is important for our custom dark theme styling
    admin = Admin(app, name='TaskManager Admin', template_mode='bootstrap4')

    # Add Views (using English names)
    admin.add_view(UserView(User, db.session, name='Users'))
    admin.add_view(TaskView(Task, db.session, name='Tasks'))
    admin.add_view(SettingsView(Settings, db.session, name='Site Settings'))

    from .routes import main
    app.register_blueprint(main)

    # Inject translations into all templates
    @app.context_processor
    def inject_language():
        # Default to 'en' if no cookie is set
        lang_code = request.cookies.get('lang', 'en')
        if lang_code not in translations:
            lang_code = 'en'
        return dict(lang=lang_code, t=translations[lang_code])

    with app.app_context():
        create_default_settings()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

def create_default_settings():
    from .models import Settings
    from sqlalchemy import inspect

    # Check if table exists to prevent crash on first run (before migrations)
    inspector = inspect(db.engine)
    if inspector.has_table("settings"):
        if not Settings.query.first():
            settings = Settings()
            db.session.add(settings)
            db.session.commit()