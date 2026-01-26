document.addEventListener('DOMContentLoaded', () => {
    // 1. АВТО-СКРЫТИЕ УВЕДОМЛЕНИЙ
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 4000);
    });

    // 2. ИНИЦИАЛИЗАЦИЯ ТЕМЫ
    // Проверяем сохраненную тему в LocalStorage
    const storedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    let activeTheme = 'light';
    if (storedTheme) {
        activeTheme = storedTheme;
    } else if (systemPrefersDark) {
        activeTheme = 'dark';
    }

    // Применяем тему
    setTheme(activeTheme);

    // 3. ЛОГИКА ПОИСКА и ФИЛЬТРОВ
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const hideCompletedFilter = document.getElementById('hideCompletedFilter');
    const taskList = document.getElementById('taskList');
    const tasks = taskList ? taskList.querySelectorAll('.task-item') : [];

    function filterTasks() {
        const searchText = searchInput.value.toLowerCase();
        const selectedCategory = categoryFilter.value;
        const hideCompleted = hideCompletedFilter.checked;

        tasks.forEach(task => {
            const content = task.getAttribute('data-content');
            const category = task.getAttribute('data-category');
            const isCompleted = task.getAttribute('data-completed') === 'true';

            const matchesSearch = content.includes(searchText);
            const matchesCategory = selectedCategory === 'all' || category === selectedCategory;
            const matchesStatus = !hideCompleted || !isCompleted;

            if (matchesSearch && matchesCategory && matchesStatus) {
                task.classList.remove('d-none');
            } else {
                task.classList.add('d-none');
            }
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', filterTasks);
        categoryFilter.addEventListener('change', filterTasks);
        hideCompletedFilter.addEventListener('change', filterTasks);
    }
});

// --- ФУНКЦИЯ УСТАНОВКИ ТЕМЫ ---
function setTheme(theme) {
    // Устанавливаем атрибут для HTML (это меняет CSS переменные)
    document.documentElement.setAttribute('data-bs-theme', theme);
    // Сохраняем выбор пользователя
    localStorage.setItem('theme', theme);

    // Обновляем иконку активной темы в меню (если меню есть)
    updateThemeIcon(theme);
}

function updateThemeIcon(theme) {
    const themeIconDisplay = document.getElementById('theme-icon-active');
    if (!themeIconDisplay) return;

    // Снимаем класс 'active' со всех пунктов
    document.querySelectorAll('[data-bs-theme-value]').forEach(el => {
        el.classList.remove('active');
        if (el.getAttribute('data-bs-theme-value') === theme) {
            el.classList.add('active');
        }
    });

    // Меняем иконку в навбаре
    let iconClass = 'bi-sun-fill';
    if (theme === 'dark') iconClass = 'bi-moon-stars-fill';
    else if (theme === 'gray') iconClass = 'bi-cloud-fill';
    else if (theme === 'casino') iconClass = 'bi-suit-club-fill';

    themeIconDisplay.className = `bi ${iconClass}`;
}


// --- ФУНКЦИИ ЗАДАЧ ---
async function toggleTask(id) {
    const row = document.getElementById(`task-${id}`);
    const icon = row.querySelector('.task-icon');
    const text = row.querySelector('.task-text');

    try {
        const response = await fetch(`/toggle/${id}`, { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            if (data.completed) {
                row.classList.add('bg-light', 'opacity-75');
                text.classList.add('text-decoration-line-through', 'text-muted');
                icon.classList.remove('bi-circle', 'text-secondary');
                icon.classList.add('bi-check-circle-fill', 'text-success');
            } else {
                row.classList.remove('bg-light', 'opacity-75');
                text.classList.remove('text-decoration-line-through', 'text-muted');
                icon.classList.remove('bi-check-circle-fill', 'text-success');
                icon.classList.add('bi-circle', 'text-secondary');
            }

            row.setAttribute('data-completed', data.completed);

            const hideCompletedFilter = document.getElementById('hideCompletedFilter');
            if (hideCompletedFilter && hideCompletedFilter.checked) {
                row.classList.add('d-none');
            }
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function toggleSubtask(subtaskId, parentTaskId) {
    const subtaskRow = document.getElementById(`subtask-${subtaskId}`);
    const label = subtaskRow.querySelector('label');
    const progressBar = document.getElementById(`progress-${parentTaskId}`);

    try {
        const response = await fetch(`/toggle_subtask/${subtaskId}`, { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            if (data.completed) {
                label.classList.add('text-decoration-line-through', 'text-muted');
            } else {
                label.classList.remove('text-decoration-line-through', 'text-muted');
            }
            if (progressBar) {
                progressBar.style.width = data.progress + '%';
            }
        }
    } catch (error) {
        console.error('Ошибка подзадачи:', error);
    }
}