async function toggleTask(id) {
    const row = document.getElementById(`task-${id}`);
    const icon = row.querySelector('.task-icon');
    const text = row.querySelector('.task-text');

    try {
        const response = await fetch(`/toggle/${id}`, { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            if (data.completed) {
                // Стала выполнена
                row.classList.add('bg-light', 'opacity-75');
                text.classList.add('text-decoration-line-through', 'text-muted');

                icon.classList.remove('bi-circle', 'text-secondary');
                icon.classList.add('bi-check-circle-fill', 'text-success');
            } else {
                // Вернули в работу
                row.classList.remove('bg-light', 'opacity-75');
                text.classList.remove('text-decoration-line-through', 'text-muted');

                icon.classList.remove('bi-check-circle-fill', 'text-success');
                icon.classList.add('bi-circle', 'text-secondary');
            }
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}