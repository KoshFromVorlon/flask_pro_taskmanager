"""
This module contains all text translations for the application.
Languages supported: English (en), Russian (ru), Ukrainian (ua).
Usage: Import this dictionary in routes or templates to serve dynamic text.
"""

translations = {
    'en': {
        # --- GENERAL ---
        'title': 'TaskMaster Pro',
        'theme_light': 'Light',
        'theme_dark': 'Dark',
        'btn_save': 'Save',
        'btn_add': 'Add',
        'btn_update': 'Update',
        'btn_delete': 'Delete',
        'btn_cancel': 'Cancel',
        'mb_label': 'MB',

        # --- NAVIGATION ---
        'login_btn': 'Login',
        'register_btn': 'Sign Up',
        'admin_btn': 'Admin Panel',
        'logout_btn': 'Logout',
        'profile_btn': 'My Profile',
        'calendar_btn': 'Calendar',

        # --- HOME / TASKS ---
        'placeholder_task': 'New task...',
        'placeholder_deadline': 'Due date',
        'placeholder_search': 'Search tasks...',
        'filter_hide': 'Hide Completed',
        'filter_all_cats': 'All Categories',
        'empty_state': 'No plans. Enjoy your freedom!',
        'deadline_prefix': 'due',
        'overdue_prefix': 'Overdue',
        'created_prefix': 'created',
        'add_step_btn': '+ Step',

        # [NEW] File Input Customization
        'choose_file': 'Choose Files',
        'no_file_selected': 'No file chosen',

        # --- EDIT MODAL (New) ---
        'label_task_name': 'Task Name',
        'label_description': 'Description',
        'label_category': 'Category',
        'label_deadline': 'Deadline',
        'label_files': 'Files',
        'label_subtasks': 'Subtasks',
        'btn_save_changes': 'Save All Changes',

        # --- CATEGORIES (Database Keys) ---
        'cat_work': 'Work',
        'cat_home': 'Home',
        'cat_study': 'Study',
        'cat_shopping': 'Shopping',
        'cat_important': 'Important',
        'cat_other': 'Other',

        # --- AUTHENTICATION ---
        'login_header': 'System Login',
        'login_label': 'Username',
        'password_label': 'Password',
        'remember_me': 'Remember me',
        'no_account': 'No account?',
        'register_link': 'Register now',
        'login_link': 'Login',

        'register_header': 'System Registration',
        'register_label': 'Username',
        'email_label': 'Email',
        'confirm_pass_label': 'Confirm Password',
        'have_account': 'Have an account?',

        # --- PROFILE ---
        'profile_header': 'Profile Settings',
        'avatar_label': 'Upload Avatar',
        'upload_btn': 'Update Photo',
        'change_pass_header': 'Change Password',
        'old_pass': 'Current Password',
        'new_pass': 'New Password',
        'files_count': 'files',
        'attach_label': 'Attach files',

        # --- FLASH MESSAGES ---
        'flash_file_type_error': 'This file type is not allowed by admin!',
        'flash_file_size_error': 'File is too big! Max allowed: ',
        'flash_user_exists': 'This user already exists!',
        'flash_register_success': 'Registration successful! Welcome.',
        'flash_login_success': 'Successfully logged in.',
        'flash_login_error': 'Login error. Check your credentials.',
        'flash_logout': 'You have logged out.',
        'flash_pass_wrong': 'Old password is incorrect.',
        'flash_pass_changed': 'Password changed successfully!',
        'flash_profile_updated': 'Profile updated successfully!',
        'flash_task_added': 'Task added!',
        'flash_task_deleted': 'Task deleted.',
        'flash_avatar_uploaded': 'Avatar updated!',
        'flash_invalid_file': 'Invalid file format (jpg, png allowed).',
    },

    'ru': {
        # --- GENERAL ---
        'title': 'TaskMaster Pro',
        'theme_light': 'Светлая',
        'theme_dark': 'Темная',
        'btn_save': 'Сохранить',
        'btn_add': 'Добавить',
        'btn_update': 'Обновить',
        'btn_delete': 'Удалить',
        'btn_cancel': 'Отмена',
        'mb_label': 'МБ',

        # --- NAVIGATION ---
        'login_btn': 'Вход',
        'register_btn': 'Регистрация',
        'admin_btn': 'Админка',
        'logout_btn': 'Выйти',
        'profile_btn': 'Мой профиль',
        'calendar_btn': 'Календарь',

        # --- HOME / TASKS ---
        'placeholder_task': 'Новая задача...',
        'placeholder_deadline': 'Срок выполнения',
        'placeholder_search': 'Поиск по задачам...',
        'filter_hide': 'Скрыть готовые',
        'filter_all_cats': 'Все категории',
        'empty_state': 'Планов нет. Наслаждайся свободой!',
        'deadline_prefix': 'до',
        'overdue_prefix': 'Просрочено',
        'created_prefix': 'созд.',
        'add_step_btn': '+ Шаг',

        # [NEW] File Input Customization
        'choose_file': 'Выбрать файлы',
        'no_file_selected': 'Файл не выбран',

        # --- EDIT MODAL (New) ---
        'label_task_name': 'Название задачи',
        'label_description': 'Описание',
        'label_category': 'Категория',
        'label_deadline': 'Дедлайн',
        'label_files': 'Файлы',
        'label_subtasks': 'Подзадачи',
        'btn_save_changes': 'Сохранить всё',

        # --- CATEGORIES ---
        'cat_work': 'Работа',
        'cat_home': 'Дом',
        'cat_study': 'Учеба',
        'cat_shopping': 'Покупки',
        'cat_important': 'Важное',
        'cat_other': 'Другое',

        # --- AUTHENTICATION ---
        'login_header': 'Вход в систему',
        'login_label': 'Логин',
        'password_label': 'Пароль',
        'remember_me': 'Запомнить меня',
        'no_account': 'Нет аккаунта?',
        'register_link': 'Зарегистрироваться',
        'login_link': 'Войти',

        'register_header': 'Регистрация в системе',
        'register_label': 'Логин',
        'email_label': 'Email',
        'confirm_pass_label': 'Повторите пароль',
        'have_account': 'Есть аккаунт?',

        # --- PROFILE ---
        'profile_header': 'Настройки профиля',
        'avatar_label': 'Загрузить аватар',
        'upload_btn': 'Обновить фото',
        'change_pass_header': 'Смена пароля',
        'old_pass': 'Текущий пароль',
        'new_pass': 'Новый пароль',
        'files_count': 'файлов',
        'attach_label': 'Прикрепить файлы',

        # --- FLASH MESSAGES ---
        'flash_file_type_error': 'Этот тип файла запрещен администратором!',
        'flash_file_size_error': 'Файл слишком большой! Максимум разрешено: ',
        'flash_user_exists': 'Такой пользователь уже существует!',
        'flash_register_success': 'Регистрация успешна! Добро пожаловать.',
        'flash_login_success': 'Вы успешно вошли!',
        'flash_login_error': 'Ошибка входа. Проверьте данные.',
        'flash_logout': 'Вы вышли из системы.',
        'flash_pass_wrong': 'Старый пароль введен неверно.',
        'flash_pass_changed': 'Пароль успешно изменен!',
        'flash_profile_updated': 'Профиль успешно обновлен!',
        'flash_task_added': 'Задача добавлена!',
        'flash_task_deleted': 'Задача удалена.',
        'flash_avatar_uploaded': 'Аватар обновлен!',
        'flash_invalid_file': 'Неверный формат файла (разрешены jpg, png).',
    },

    'ua': {
        # --- GENERAL ---
        'title': 'TaskMaster Pro',
        'theme_light': 'Світла',
        'theme_dark': 'Темна',
        'btn_save': 'Зберегти',
        'btn_add': 'Додати',
        'btn_update': 'Оновити',
        'btn_delete': 'Видалити',
        'btn_cancel': 'Скасувати',
        'mb_label': 'МБ',

        # --- NAVIGATION ---
        'login_btn': 'Вхід',
        'register_btn': 'Реєстрація',
        'admin_btn': 'Адмінка',
        'logout_btn': 'Вийти',
        'profile_btn': 'Мій профіль',
        'calendar_btn': 'Календар',

        # --- HOME / TASKS ---
        'placeholder_task': 'Нове завдання...',
        'placeholder_deadline': 'Термін виконання',
        'placeholder_search': 'Пошук завдань...',
        'filter_hide': 'Приховати готові',
        'filter_all_cats': 'Всі категорії',
        'empty_state': 'Планів немає. Насолоджуйтесь свободою!',
        'deadline_prefix': 'до',
        'overdue_prefix': 'Прострочено',
        'created_prefix': 'створ.',
        'add_step_btn': '+ Крок',

        # [NEW] File Input Customization
        'choose_file': 'Обрати файли',
        'no_file_selected': 'Файл не обрано',

        # --- EDIT MODAL (New) ---
        'label_task_name': 'Назва завдання',
        'label_description': 'Опис',
        'label_category': 'Категория',
        'label_deadline': 'Дедлайн',
        'label_files': 'Файли',
        'label_subtasks': 'Підзавдання',
        'btn_save_changes': 'Зберегти все',

        # --- CATEGORIES ---
        'cat_work': 'Робота',
        'cat_home': 'Дім',
        'cat_study': 'Навчання',
        'cat_shopping': 'Покупки',
        'cat_important': 'Важливе',
        'cat_other': 'Інше',

        # --- AUTHENTICATION ---
        'login_header': 'Вхід до системи',
        'login_label': 'Логін',
        'password_label': 'Пароль',
        'remember_me': 'Запам\'ятати мене',
        'no_account': 'Немає акаунту?',
        'register_link': 'Зареєструватися',
        'login_link': 'Увійти',

        'register_header': 'Реєстрація в системі',
        'register_label': 'Логін',
        'email_label': 'Email',
        'confirm_pass_label': 'Повторіть пароль',
        'have_account': 'Є акаунт?',

        # --- PROFILE ---
        'profile_header': 'Налаштування профілю',
        'avatar_label': 'Завантажити аватар',
        'upload_btn': 'Оновити фото',
        'change_pass_header': 'Зміна паролю',
        'old_pass': 'Поточний пароль',
        'new_pass': 'Новий пароль',
        'files_count': 'файлів',
        'attach_label': 'Прикріпити файли',

        # --- FLASH MESSAGES ---
        'flash_file_type_error': 'Цей тип файлу заборонено адміністратором!',
        'flash_file_size_error': 'Файл занадто великий! Максимум дозволено: ',
        'flash_user_exists': 'Такий користувач вже існує!',
        'flash_register_success': 'Реєстрація успішна! Ласкаво просимо.',
        'flash_login_success': 'Ви успішно увійшли!',
        'flash_login_error': 'Помилка входу. Перевірте дані.',
        'flash_logout': 'Ви вийшли із системи.',
        'flash_pass_wrong': 'Старий пароль введено невірно.',
        'flash_pass_changed': 'Пароль успішно змінено!',
        'flash_profile_updated': 'Профіль успішно оновлено!',
        'flash_task_added': 'Завдання додано!',
        'flash_task_deleted': 'Завдання видалено.',
        'flash_avatar_uploaded': 'Аватар оновлено!',
        'flash_invalid_file': 'Невірний формат файлу (дозволено jpg, png).',
    }
}