from app import create_app
from flask_migrate import upgrade  # <--- Добавили импорт

app = create_app()

# <--- Добавляем блок автоматического обновления базы
with app.app_context():
    upgrade()

if __name__ == '__main__':
    app.run()