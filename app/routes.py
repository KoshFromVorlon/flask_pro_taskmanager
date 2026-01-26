from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db
from .models import User, Task

main = Blueprint('main', __name__)


# --- АВТОРИЗАЦИЯ ---
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Такой пользователь уже существует!', 'error')
            return redirect(url_for('main.register'))

        user = User(username=username, password=generate_password_hash(password, method='scrypt'))
        if User.query.count() == 0: user.is_admin = True

        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Регистрация успешна! Добро пожаловать.', 'success')
        return redirect(url_for('main.index'))

    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('main.index'))
        flash('Ошибка входа. Проверьте данные.', 'error')
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('main.login'))


@main.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        if not check_password_hash(current_user.password, old_password):
            flash('Старый пароль введен неверно.', 'error')
            return redirect(url_for('main.change_password'))

        current_user.password = generate_password_hash(new_password, method='scrypt')
        db.session.commit()
        flash('Пароль успешно изменен!', 'success')
        return redirect(url_for('main.index'))

    return render_template('change_password.html')


# --- ЗАДАЧИ ---
@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        category = request.form.get('category')
        deadline_str = request.form.get('deadline')  # Получаем строку "2023-10-30T14:30"

        if content:
            # Превращаем строку в объект даты (если она была заполнена)
            deadline_obj = None
            if deadline_str:
                try:
                    deadline_obj = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
                except ValueError:
                    pass  # Если пришла ерунда, просто игнорируем

            new_task = Task(content=content, category=category, deadline=deadline_obj, author=current_user)
            db.session.add(new_task)
            db.session.commit()
            flash('Задача добавлена!', 'success')
            return redirect(url_for('main.index'))

    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.completed, Task.deadline,
                                                                   Task.date_created).all()
    # Передаем "now" в шаблон, чтобы сравнивать даты
    return render_template('index.html', tasks=tasks, now=datetime.now())


@main.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash('Задача удалена.', 'success')
    return redirect(url_for('main.index'))


@main.route('/toggle/<int:id>', methods=['POST'])
@login_required
def toggle(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        task.completed = not task.completed
        db.session.commit()
        return jsonify({'success': True, 'completed': task.completed})
    return jsonify({'success': False})