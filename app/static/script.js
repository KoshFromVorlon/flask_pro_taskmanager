document.addEventListener('DOMContentLoaded', () => {
    // --- 1. АВТОМАТИЧЕСКОЕ СКРЫТИЕ СООБЩЕНИЙ ---

    // Находим все уведомления, которые можно закрыть
    const alerts = document.querySelectorAll('.alert-dismissible');

    alerts.forEach(alert => {
        // Запускаем таймер на 4000 мс (4 секунды)
        setTimeout(() => {
            // Проверяем, существует ли элемент (вдруг пользователь закрыл его раньше)
            if (alert) {
                // Используем Bootstrap API для красивого исчезновения
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 4000);
    });
});

// --- 2. ЛОГИКА ЗАДАЧ (AJAX) ---

async function toggleTask(id) {
    // Находим элементы строки задачи
    const row = document.getElementById(`task-${id}`);
    const icon = row.querySelector('.task-icon');
    const text = row.querySelector('.task-text');

    try {
        // Отправляем запрос на сервер
        const response = await fetch(`/toggle/${id}`, { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            // Обновляем вид в зависимости от нового статуса
            if (data.completed) {
                // ЗАДАЧА ВЫПОЛНЕНА
                row.classList.add('bg-light', 'opacity-75');
                text.classList.add('text-decoration-line-through', 'text-muted');

                // Меняем кружок на зеленую галочку
                icon.classList.remove('bi-circle', 'text-secondary');
                icon.classList.add('bi-check-circle-fill', 'text-success');
            } else {
                // ЗАДАЧА АКТИВНА (ВЕРНУЛИ)
                row.classList.remove('bg-light', 'opacity-75');
                text.classList.remove('text-decoration-line-through', 'text-muted');

                // Меняем галочку на серый кружок
                icon.classList.remove('bi-check-circle-fill', 'text-success');
                icon.classList.add('bi-circle', 'text-secondary');
            }
        }
    } catch (error) {
        console.error('Ошибка при обновлении задачи:', error);
    }
}