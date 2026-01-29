from app import create_app
from flask_migrate import upgrade

app = create_app()

# Apply database migrations automatically on application startup
# This ensures the database schema is always up-to-date when the server restarts
with app.app_context():
    upgrade()

if __name__ == '__main__':
    app.run()