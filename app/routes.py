import os
import secrets
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from . import db
from .models import User, Task, Subtask, Attachment, Settings
from .translations import translations

main = Blueprint('main', __name__)


def get_text(key):
    lang = request.cookies.get('lang', 'ru')
    if lang not in translations: lang = 'ru'
    return translations[lang].get(key, key)


# --- ПРОВЕРКИ ФАЙЛОВ ---
def allowed_file(filename):
    settings = Settings.get_settings()
    allowed = set(ext.strip().lower() for ext in settings.allowed_extensions.split(','))
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def check_file_size(file):
    settings = Settings.get_settings()
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)
    return file_length <= (settings.max_file_size_mb * 1024 * 1024)


# --- СОХРАНЕНИЕ ФАЙЛОВ ---
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    folder_path = os.path.join(current_app.root_path, 'static', 'avatars')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    picture_path = os.path.join(folder_path, picture_fn)
    form_picture.save(picture_path)
    return picture_fn


def save_attachment(file_obj):
    original_name = secure_filename(file_obj.filename)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(original_name)
    secure_name = random_hex + f_ext
    folder_path = os.path.join(current_app.root_path, 'static', 'uploads')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    path = os.path.join(folder_path, secure_name)
    file_obj.save(path)
    return secure_name, original_name


@main.route('/set-language/<lang_code>')
def set_language(lang_code):
    if lang_code not in translations: lang_code = 'ru'
    referrer = request.referrer or url_for('main.index')
    resp = make_response(redirect(referrer))
    resp.set_cookie('lang', lang_code, max_age=30 * 24 * 60 * 60)
    return resp


# --- AUTH ---
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash(get_text('flash_user_exists'), 'error')
            return redirect(url_for('main.register'))
        user = User(username=username, password=generate_password_hash(password, method='scrypt'))
        if User.query.count() == 0:
            user.is_admin = True
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(get_text('flash_register_success'), 'success')
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
            flash(get_text('flash_login_success'), 'success')
            return redirect(url_for('main.index'))
        flash(get_text('flash_login_error'), 'error')
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # 1. Обновление Аватарки
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and file.filename != '':
                allowed_imgs = {'png', 'jpg', 'jpeg', 'gif'}
                if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_imgs:
                    try:
                        filename = save_picture(file)
                        current_user.avatar = filename
                        db.session.commit()
                        flash(get_text('flash_avatar_uploaded'), 'success')
                    except Exception as e:
                        flash(f"Error: {e}", 'error')
                else:
                    flash(get_text('flash_invalid_file'), 'error')

        # 2. Обновление пароля
        if 'old_password' in request.form and request.form['old_password']:
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            if not check_password_hash(current_user.password, old_password):
                flash(get_text('flash_pass_wrong'), 'error')
            else:
                current_user.password = generate_password_hash(new_password, method='scrypt')
                db.session.commit()
                flash(get_text('flash_pass_changed'), 'success')

        # 3. [НОВОЕ] Обновление имени пользователя (для теста test_account_update)
        new_username = request.form.get('username')
        if new_username and new_username != current_user.username:
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user:
                flash(get_text('flash_user_exists'), 'error')
            else:
                current_user.username = new_username
                db.session.commit()
                flash(get_text('flash_profile_updated'), 'success')  # Нужен ключ в translations

        return redirect(url_for('main.profile'))

    image_file = url_for('static', filename='avatars/' + current_user.avatar)
    return render_template('profile.html', image_file=image_file)


# --- TASKS ---
@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        category_key = request.form.get('category')
        deadline_str = request.form.get('deadline')

        if content:
            deadline_obj = None
            if deadline_str:
                try:
                    deadline_obj = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
                except ValueError:
                    pass

            new_task = Task(content=content, category=category_key, deadline=deadline_obj, author=current_user)
            db.session.add(new_task)
            db.session.flush()

            files = request.files.getlist('files')
            settings = Settings.get_settings()

            for file in files:
                if file and file.filename != '':
                    if not allowed_file(file.filename):
                        flash(get_text('flash_file_type_error') + f" ({file.filename})", 'error')
                        continue
                    if not check_file_size(file):
                        flash(get_text(
                            'flash_file_size_error') + f"{settings.max_file_size_mb} {get_text('mb_label')} ({file.filename})",
                              'error')
                        continue
                    try:
                        secure_name, original_name = save_attachment(file)
                        attachment = Attachment(filename=secure_name, original_name=original_name, parent_task=new_task)
                        db.session.add(attachment)
                    except Exception as e:
                        flash(f"Error saving file: {e}", 'error')

            db.session.commit()
            flash(get_text('flash_task_added'), 'success')
            return redirect(url_for('main.index'))

    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.position.asc(), Task.date_created.desc()).all()
    return render_template('index.html', tasks=tasks, now=datetime.now())


# [НОВОЕ] Маршрут для редактирования задачи (для теста test_update_task)
@main.route('/task/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Access denied'}), 403

    content = request.form.get('content')
    category = request.form.get('category')

    if content:
        task.content = content
    if category:
        task.category = category

    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/reorder', methods=['POST'])
@login_required
def reorder_tasks():
    data = request.get_json()
    task_ids = data.get('task_ids', [])
    user_tasks = {task.id: task for task in Task.query.filter_by(user_id=current_user.id).all()}

    for index, task_id in enumerate(task_ids):
        t_id = int(task_id)
        if t_id in user_tasks:
            user_tasks[t_id].position = index

    db.session.commit()
    return jsonify({'success': True})


@main.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash(get_text('flash_task_deleted'), 'success')
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


@main.route('/task/<int:task_id>/add_subtask', methods=['POST'])
@login_required
def add_subtask(task_id):
    task = Task.query.get_or_404(task_id)
    content = request.form.get('subtask_content')
    if task.user_id == current_user.id and content:
        subtask = Subtask(content=content, parent_task=task)
        db.session.add(subtask)
        db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/toggle_subtask/<int:subtask_id>', methods=['POST'])
@login_required
def toggle_subtask(subtask_id):
    subtask = Subtask.query.get_or_404(subtask_id)
    if subtask.parent_task.user_id == current_user.id:
        subtask.completed = not subtask.completed
        db.session.commit()
        progress = subtask.parent_task.get_progress()
        return jsonify({'success': True, 'completed': subtask.completed, 'progress': progress})
    return jsonify({'success': False})


@main.route('/delete_subtask/<int:subtask_id>')
@login_required
def delete_subtask(subtask_id):
    subtask = Subtask.query.get_or_404(subtask_id)
    if subtask.parent_task.user_id == current_user.id:
        db.session.delete(subtask)
        db.session.commit()
    return redirect(url_for('main.index'))


# --- CALENDAR ---
@main.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')


@main.route('/api/events')
@login_required
def get_events():
    tasks = Task.query.filter(Task.user_id == current_user.id, Task.deadline != None).all()
    events = []

    category_colors = {
        get_text('cat_work'): '#0d6efd',
        get_text('cat_home'): '#198754',
        get_text('cat_study'): '#0dcaf0',
        get_text('cat_shopping'): '#ffc107',
        get_text('cat_important'): '#dc3545',
        get_text('cat_other'): '#6c757d'
    }

    light_colors = ['#ffc107', '#0dcaf0']

    for task in tasks:
        bg_color = category_colors.get(task.category, '#6c757d')
        text_color = '#000000' if bg_color in light_colors else '#ffffff'

        if task.deadline < datetime.now() and not task.completed:
            bg_color = '#dc3545'
            text_color = '#ffffff'

        if task.completed:
            bg_color = '#20c997'
            text_color = '#ffffff'

        events.append({
            'title': task.content,
            'start': task.deadline.isoformat(),
            'backgroundColor': bg_color,
            'borderColor': bg_color,
            'textColor': text_color,
            'url': f'/#task-{task.id}',
            'allDay': False
        })
    return jsonify(events)