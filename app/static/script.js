async function toggleTask(id) {
    const row = document.getElementById(`task-${id}`);
    const checkbox = row.querySelector('input[type="checkbox"]');

    try {
        const response = await fetch(`/toggle/${id}`, { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            if (data.completed) {
                row.classList.add('bg-light', 'text-decoration-line-through', 'text-muted');
                checkbox.checked = true;
            } else {
                row.classList.remove('bg-light', 'text-decoration-line-through', 'text-muted');
                checkbox.checked = false;
            }
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}