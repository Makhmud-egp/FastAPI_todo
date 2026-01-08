// ============================================
// 1. ADD TODO - TUZATILDI
// ============================================
const todoForm = document.getElementById('todoForm');
if (todoForm) {
    todoForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        const payload = {
            title: data.title,
            description: data.description,
            priority: parseInt(data.priority),
            complete: false
        };

        try {
            // O'ZGARDI: /todos/todo -> /todos/create
            const response = await fetch('/todos/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                form.reset();
                // QOSHILDI: Muvaffaqiyatli xabar va sahifani yangilash
                alert('Todo successfully created!');
                window.location.href = '/todos/todo-page';
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}

// ============================================
// 2. EDIT TODO - TUZATILDI
// ============================================
const editTodoForm = document.getElementById('editTodoForm');
if (editTodoForm) {
    editTodoForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        var url = window.location.pathname;
        const todoId = url.substring(url.lastIndexOf('/') + 1);

        const payload = {
            title: data.title,
            description: data.description,
            priority: parseInt(data.priority),
            complete: data.complete === "on"
        };

        try {
            const token = getCookie('access_token');
            console.log(token);
            if (!token) {
                throw new Error('Authentication token not found');
            }

            console.log(`Todo ID: ${todoId}`);

            // O'ZGARDI: /todos/todo/${todoId} -> /todos/update/${todoId}
            const response = await fetch(`/todos/update/${todoId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                // QOSHILDI: Muvaffaqiyatli xabar
                alert('Todo successfully updated!');
                window.location.href = '/todos/todo-page';
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });

    // ============================================
    // 3. DELETE TODO - TUZATILDI
    // ============================================
    const deleteButton = document.getElementById('deleteButton');
    if (deleteButton) {
        deleteButton.addEventListener('click', async function () {
            // QOSHILDI: Delete qilishdan oldin tasdiqlash
            if (!confirm('Are you sure you want to delete this todo?')) {
                return;
            }

            var url = window.location.pathname;
            const todoId = url.substring(url.lastIndexOf('/') + 1);

            try {
                const token = getCookie('access_token');
                if (!token) {
                    throw new Error('Authentication token not found');
                }

                // O'ZGARDI: /todos/todo/${todoId} -> /todos/delete/${todoId}
                const response = await fetch(`/todos/delete/${todoId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    alert('Todo successfully deleted!');
                    window.location.href = '/todos/todo-page';
                } else {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }
}

// ============================================
// 4. LOGIN - TO'G'RI (o'zgarmagan)
// ============================================
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);

        const payload = new URLSearchParams();
        for (const [key, value] of formData.entries()) {
            payload.append(key, value);
        }

        try {
            const response = await fetch('/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: payload.toString()
            });

            if (response.ok) {
                const data = await response.json();
                logout(); // Eski tokenlarni o'chirish
                document.cookie = `access_token=${data.access_token}; path=/`;
                window.location.href = '/todos/todo-page';
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}

// ============================================
// 5. REGISTER - TO'G'RI (o'zgarmagan)
// ============================================
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        if (data.password !== data.password2) {
            alert("Passwords do not match");
            return;
        }

        const payload = {
            email: data.email,
            username: data.username,
            first_name: data.firstname,
            last_name: data.lastname,
            role: data.role,
            phone_number: data.phone_number,
            password: data.password
        };

        try {
            const response = await fetch('/auth/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                alert('Registration successful! Please login.');
                window.location.href = '/auth/login-page';
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.message || errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}

// ============================================
// HELPER FUNCTIONS
// ============================================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function logout() {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    }
    window.location.href = '/auth/login-page';
}