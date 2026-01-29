# 🚀 TaskMaster Pro

![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0-green.svg)
![Docker](https://img.shields.io/badge/docker-available-blue)
![PostgreSQL](https://img.shields.io/badge/postgres-15-blue)
![Coverage](https://img.shields.io/badge/coverage-77%25-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

**TaskMaster Pro** is a modern, feature-rich web task manager with support for categories, subtasks, file attachments, 
and an interactive calendar. The application is built with **Flask**, uses **PostgreSQL** for data storage, and is 
fully containerized with **Docker**.

> 💡 **Demo:** [Link to deployment] | **Status:** Stable

## 🖼️ Screenshots

### 📊 Dashboard
![Dashboard](screenshots/dashboard_screen.png)

### 📅 Calendar View
![Calendar](screenshots/calendar_view.png)

### 🔐 Registration
![Register](screenshots/register_screen.png)

## ✨ Features

- ✅ **Task Management:** Full CRUD cycle (Create, Read, Update, Delete).
- 📂 **Categories:** Color-coded categories (Work, Home, Study, Shopping, etc.).
- 📅 **Interactive Calendar:** Visual deadline tracking powered by FullCalendar.
- 📎 **Attachments:** Upload files and images to specific tasks.
- 🏗️ **Subtasks:** Break down complex tasks into smaller steps with a progress bar.
- 👤 **User Profile:** Manage avatar, username, and password securely.
- 🌐 **Localization:** Multi-language support (**English, Russian, Ukrainian**).
- 🐳 **Docker:** One-command deployment.

## 🛠️ Tech Stack

* **Backend:** Python 3.9, Flask, SQLAlchemy, Flask-Login, Flask-Migrate.
* **Database:** PostgreSQL (Production), SQLite (Dev/Test).
* **Frontend:** Bootstrap 5, Jinja2, JavaScript (Fetch API, SortableJS).
* **Testing:** Pytest, Coverage (77% test coverage).
* **DevOps:** Docker, Docker Compose, GitHub Actions.

## 🚀 Getting Started (Docker)

This is the recommended way to run the application. You need **Docker** and **Docker Compose** installed.

1. Clone the repository:
```bash
git clone [https://github.com/KoshFromVorlon/flask_pro_taskmanager.git](https://github.com/KoshFromVorlon/flask_pro_taskmanager.git)
cd flask_pro_taskmanager
```

2. Run the application:
Start the containers (Web + DB):
```bash
docker-compose up --build
```
3. Database Migrations
Migrations run automatically on startup (run.py), but you can run them manually if needed:
```bash
docker-compose exec web flask db upgrade
```

4. Running Tests
Run the test suite inside the container:
```bash
docker-compose exec web coverage run -m pytest
```

View the coverage report:
```bash
docker-compose exec web coverage report
```

## 📂 Project Structure
```text
flask_pro_taskmanager/
├── .github/
│   └── workflows/
│       └── tests.yml    # CI/CD Configuration (GitHub Actions)
├── app/
│   ├── static/
│   │   ├── avatars/     # User uploaded avatars
│   │   ├── uploads/     # Task attachments
│   │   ├── script.js    # Frontend logic (Drag-and-Drop, Calendar, API)
│   │   └── style.css    # Custom styles
│   ├── templates/
│   │   ├── admin/       # Flask-Admin templates
│   │   ├── base.html    # Base layout (Navbar, Flash messages)
│   │   ├── calendar.html
│   │   ├── index.html   # Main dashboard (Task list)
│   │   ├── login.html
│   │   ├── profile.html # User settings (Avatar, Password, Username)
│   │   └── register.html
│   ├── __init__.py      # App Factory & Initialization
│   ├── models.py        # Database Models (User, Task, Subtask, Attachment)
│   ├── routes.py        # Main application logic & endpoints
│   └── translations.py  # Dictionary for I18n (EN/RU/UA)
├── migrations/          # Database migration versions (Alembic)
├── tests/               # Test Suite (Pytest)
│   ├── conftest.py      # Fixtures & Test DB config
│   ├── test_api.py      # Calendar API tests
│   ├── test_extended.py # Profile & Edge cases
│   ├── test_models.py   # DB Model tests
│   ├── test_routes.py   # Route status checks
│   ├── test_security.py # Auth & Permission tests
│   └── test_tasks.py    # Task logic tests
├── .dockerignore        # Docker build exclusions
├── config.py            # Environment configuration
├── Dockerfile           # Application container build instructions
├── docker-compose.yml   # Service orchestration
├── LICENSE              # MIT License
├── requirements.txt     # Python dependencies
└── run.py               # Entry point
```
