/**
 * Main Client-Side Logic
 * Handles: Auto-hiding alerts, Theme switching, Drag & Drop, Filtering, and AJAX toggles.
 */

document.addEventListener('DOMContentLoaded', () => {

    // 1. Auto-hide Flash Messages
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 4000); // 4 seconds delay
    });

    // 2. Initialize Theme (Dark/Light)
    const storedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    let activeTheme = storedTheme || (systemPrefersDark ? 'dark' : 'light');
    setTheme(activeTheme);

    // 3. Drag and Drop (SortableJS)
    const taskList = document.getElementById('taskList');
    if (taskList) {
        new Sortable(taskList, {
            animation: 150, // Smooth animation
            handle: '.drag-handle', // Drag using this specific icon only
            ghostClass: 'bg-body-secondary', // Class applied to the placeholder

            onEnd: function (evt) {
                // Collect new order of IDs
                const itemEls = taskList.querySelectorAll('.task-item');
                const taskIds = Array.from(itemEls).map(el => el.getAttribute('data-task-id'));

                // Send new order to server
                fetch('/reorder', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ task_ids: taskIds })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log('Order saved successfully');
                    }
                })
                .catch(error => console.error('Error saving order:', error));
            }
        });
    }

    // 4. Search and Filtering
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const hideCompletedFilter = document.getElementById('hideCompletedFilter');
    const tasks = taskList ? taskList.querySelectorAll('.task-item') : [];

    function filterTasks() {
        const searchText = searchInput.value.toLowerCase();
        const selectedCategory = categoryFilter.value;
        const hideCompleted = hideCompletedFilter.checked;

        tasks.forEach(task => {
            const content = task.getAttribute('data-content');
            const category = task.getAttribute('data-category'); // Expecting key like 'cat_work'
            const isCompleted = task.getAttribute('data-completed') === 'true';

            const matchesSearch = content.includes(searchText);
            // 'all' matches everything, otherwise check exact key match
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

// --- Theme Helper Functions ---

function setTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem('theme', theme);
    updateThemeIcon(theme);
}

function updateThemeIcon(theme) {
    const themeIconDisplay = document.getElementById('theme-icon-active');
    if (!themeIconDisplay) return;

    document.querySelectorAll('[data-bs-theme-value]').forEach(el => {
        el.classList.remove('active');
        if (el.getAttribute('data-bs-theme-value') === theme) {
            el.classList.add('active');
        }
    });

    if (theme === 'dark') {
        themeIconDisplay.className = 'bi bi-moon-stars-fill';
    } else {
        themeIconDisplay.className = 'bi bi-sun-fill';
    }
}

// --- AJAX Toggles (Task Completion) ---

async function toggleTask(id) {
    const row = document.getElementById(`task-${id}`);
    const icon = row.querySelector('.task-icon');
    const text = row.querySelector('.task-text');

    try {
        const response = await fetch(`/toggle/${id}`, { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            if (data.completed) {
                row.classList.add('list-group-item-secondary', 'opacity-75');
                text.classList.add('text-decoration-line-through', 'text-muted');
                icon.classList.remove('bi-circle', 'text-secondary');
                icon.classList.add('bi-check-circle-fill', 'text-success');
            } else {
                row.classList.remove('list-group-item-secondary', 'opacity-75');
                text.classList.remove('text-decoration-line-through', 'text-muted');
                icon.classList.remove('bi-check-circle-fill', 'text-success');
                icon.classList.add('bi-circle', 'text-secondary');
            }
            row.setAttribute('data-completed', data.completed);

            // Re-apply filter immediately if "Hide Completed" is on
            const hideCompletedFilter = document.getElementById('hideCompletedFilter');
            if (hideCompletedFilter && hideCompletedFilter.checked) {
                row.classList.add('d-none');
            }
        }
    } catch (error) {
        console.error('Task toggle error:', error);
    }
}

// --- AJAX Toggles (Subtask Completion) ---

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
        console.error('Subtask toggle error:', error);
    }
}