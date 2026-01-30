/**
 * Main Client-Side Logic
 */

document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Custom File Input Logic ---
    const fileInput = document.getElementById('customFile');
    const fileNameDisplay = document.getElementById('fileNameDisplay');

    if (fileInput && fileNameDisplay) {
        fileInput.addEventListener('change', function(e) {
            if (fileInput.files.length > 0) {
                if (fileInput.files.length === 1) {
                    fileNameDisplay.value = fileInput.files[0].name;
                } else {
                    fileNameDisplay.value = fileInput.files.length + ' files selected';
                }
                fileNameDisplay.classList.remove('text-muted');
            } else {
                fileNameDisplay.value = '';
                fileNameDisplay.classList.add('text-muted');
            }
        });
    }

    // --- 2. Auto-hide Flash Messages ---
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 4000);
    });

    // --- 3. Initialize Theme ---
    const storedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    let activeTheme = storedTheme || (systemPrefersDark ? 'dark' : 'light');
    setTheme(activeTheme);

    // --- 4. Drag and Drop (SortableJS) ---
    const taskList = document.getElementById('taskList');
    if (taskList) {
        new Sortable(taskList, {
            animation: 150,
            handle: '.list-group-item',
            onEnd: function (evt) {
                var order = this.toArray();
                var taskIds = order.map(id => id.replace('task-', ''));

                fetch('/reorder', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ task_ids: taskIds })
                });
            }
        });
    }

    // --- 5. Search and Filtering (Updated for Visibility Toggle) ---

    // Check initial state from LocalStorage and update UI
    const isHidden = localStorage.getItem('hideCompleted') === 'true';
    updateToggleButtonUI(isHidden);

    // Attach event listeners for search and categories
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');

    if (searchInput) {
        searchInput.addEventListener('input', window.filterTasks);
    }
    if (categoryFilter) {
        categoryFilter.addEventListener('change', window.filterTasks);
    }

    // Run filter on load to apply "Hide Completed" state
    window.filterTasks();
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

// --- GLOBAL FUNCTIONS ---

// 1. Filter Tasks Logic (Global)
window.filterTasks = function() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const taskList = document.getElementById('taskList');
    const tasks = taskList ? taskList.querySelectorAll('.task-item') : [];

    const searchText = searchInput ? searchInput.value.toLowerCase() : '';
    const selectedCategory = categoryFilter ? categoryFilter.value : 'all';

    // Read directly from storage to allow persistent state
    const hideCompleted = localStorage.getItem('hideCompleted') === 'true';

    tasks.forEach(task => {
        const content = task.getAttribute('data-content') || '';
        const category = task.getAttribute('data-category');
        const isCompleted = task.getAttribute('data-completed') === 'true';

        const matchesSearch = content.includes(searchText);
        const matchesCategory = selectedCategory === 'all' || category === selectedCategory;

        // Logic: If hideCompleted is active, show only if NOT completed
        const matchesStatus = !hideCompleted || !isCompleted;

        if (matchesSearch && matchesCategory && matchesStatus) {
            task.classList.remove('d-none');
        } else {
            task.classList.add('d-none');
        }
    });
};

// 2. Toggle Completed Visibility (Global, called by button)
window.toggleCompletedTasks = function() {
    const currentState = localStorage.getItem('hideCompleted') === 'true';
    const newState = !currentState;

    // Save to local storage
    localStorage.setItem('hideCompleted', newState);

    // Update Button UI
    updateToggleButtonUI(newState);

    // Re-run filter logic
    window.filterTasks();
};

function updateToggleButtonUI(hide) {
    const btn = document.getElementById('toggleCompletedBtn');
    if (!btn) return;

    const icon = btn.querySelector('i');

    if (hide) {
        btn.classList.add('active', 'btn-secondary');
        btn.classList.remove('btn-outline-secondary');
        if(icon) {
            icon.classList.remove('bi-eye-slash');
            icon.classList.add('bi-eye');
        }
    } else {
        btn.classList.remove('active', 'btn-secondary');
        btn.classList.add('btn-outline-secondary');
        if(icon) {
            icon.classList.remove('bi-eye');
            icon.classList.add('bi-eye-slash');
        }
    }
}

// 3. Open Edit Modal
window.openEditModal = function(taskId) {
    document.getElementById('editFilesList').innerHTML = 'Loading...';
    document.getElementById('editSubtasksList').innerHTML = '';

    fetch(`/task/${taskId}/details`)
        .then(response => response.json())
        .then(data => {
            if (data.error) return alert(data.error);

            document.getElementById('editTaskId').value = data.id;
            document.getElementById('editTaskContent').value = data.content;
            document.getElementById('editTaskDesc').value = data.description;
            document.getElementById('editTaskCategory').value = data.category;
            document.getElementById('editTaskDeadline').value = data.deadline ? data.deadline.slice(0, 16) : '';

            // Render files
            const filesContainer = document.getElementById('editFilesList');
            filesContainer.innerHTML = '';
            if (data.files.length === 0) {
                filesContainer.innerHTML = '<small class="text-muted">No files attached.</small>';
            }
            data.files.forEach(file => {
                filesContainer.innerHTML += `
                    <div class="d-flex justify-content-between align-items-center mb-1 bg-light p-2 rounded" id="file-row-${file.id}">
                        <a href="${file.url}" target="_blank" class="text-truncate" style="max-width: 300px;">${file.name}</a>
                        <button type="button" class="btn btn-sm btn-danger py-0" onclick="deleteFile(${file.id})">❌</button>
                    </div>
                `;
            });

            // Render subtasks
            const subtasksContainer = document.getElementById('editSubtasksList');
            subtasksContainer.innerHTML = '';
            if (data.subtasks.length === 0) {
                subtasksContainer.innerHTML = '<small class="text-muted">No subtasks.</small>';
            }
            data.subtasks.forEach(sub => {
                subtasksContainer.innerHTML += `
                    <div class="input-group mb-2">
                        <div class="input-group-text">
                            <input class="form-check-input mt-0" type="checkbox" ${sub.completed ? 'checked' : ''} disabled>
                        </div>
                        <input type="text" class="form-control" value="${sub.content}" onchange="updateSubtaskText(${sub.id}, this.value)">
                    </div>
                `;
            });

            new bootstrap.Modal(document.getElementById('editTaskModal')).show();
        });
};

// 4. Save Changes
window.saveTaskChanges = function() {
    const taskId = document.getElementById('editTaskId').value;
    const form = document.getElementById('editTaskForm');
    const formData = new FormData(form);

    fetch(`/task/${taskId}/full_update`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Error saving changes');
        }
    });
};

// 5. Delete File
window.deleteFile = function(attachmentId) {
    if (!confirm('Permanently delete this file?')) return;
    fetch(`/attachment/${attachmentId}/delete`, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const row = document.getElementById(`file-row-${attachmentId}`);
                if (row) row.remove();
            } else {
                alert('Error deleting file');
            }
        });
};

// 6. Update Subtask Text
window.updateSubtaskText = function(subtaskId, newText) {
    fetch(`/subtask/${subtaskId}/update_text`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ content: newText })
    });
};

// 7. Toggle Task
window.toggleTask = function(taskId) {
    fetch(`/toggle/${taskId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) location.reload();
        });
};

// 8. Toggle Subtask
window.toggleSubtask = function(subId, parentTaskId) {
    fetch(`/toggle_subtask/${subId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) location.reload();
        });
};