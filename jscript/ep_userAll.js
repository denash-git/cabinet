const getTable = document.querySelector('.content');

getTable.addEventListener('click', async function(event) {

    if (event.target.classList.contains('deleteBtn')) {

        if (!confirm('Вы уверены, заблокировать пользователя?')) {
            return;
        }

        const userId = event.target.dataset.userId;
        try {
            const response = await fetch(`/ep/del/${userId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Ошибка при блокировке пользователя.');
            }

            const data = await response.text();

            alert('Пользователь успешно заблокирован.');

            event.target.closest('tr').remove(); // удаление строки

        } catch (error) {
            alert(error.message);
        }
    }
});