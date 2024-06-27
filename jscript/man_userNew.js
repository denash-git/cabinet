document.getElementById('submit').addEventListener('click', function(event) {
    event.preventDefault(); // Предотвращаем обычную отправку формы

    const username = document.getElementById('username').value;
    const role = document.getElementById('role').value;

    const data = { username, role };

    fetch('/man/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка при добавлении пользователя.');
        }
        return response.json();
    })
    .then(data => {
        alert('Пользователь успешно добавлен.');
        console.log('Success:', data);
        // Очищаем форму
        document.getElementById('addUserForm').reset();
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message);
    });
});
