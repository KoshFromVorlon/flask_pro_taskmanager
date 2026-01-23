from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Task

main = Blueprint('main', __name__)


# --- АВТОРИЗАЦИЯ ---
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Создаем юзера (пароль хешируем!)
        user = User(username=username, password=generate_password_hash(password, method='scrypt'))
        # ПЕРВЫЙ зарегистрированный станет админом автоматически для теста
        if User.query.count() == 0:
            user.is_admin = True

        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('main.index'))
        except:
            flash('Такой пользователь уже есть')
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Неверный логин или пароль')
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


# --- ЗАДАЧИ ---
@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_task = Task(content=content, author=current_user)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('main.index'))

    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.date_created.desc()).all()
    return render_template('index.html', tasks=tasks, name=current_user.username)


# --- API ДЛЯ JS ---
@main.route('/toggle/<int:id>', methods=['POST'])
@login_required
def toggle(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        task.completed = not task.completed
        db.session.commit()
        return jsonify({'success': True, 'completed': task.completed})
    return jsonify({'success': False})
