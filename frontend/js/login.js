document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('token', data.token);
            document.getElementById('message').textContent = 'Login successful!';
            document.getElementById('message').style.color = 'green';
            setTimeout(() => {
                window.location.href = 'index.html';  // Redirect to the index.html page
            }, 2000);
        } else {
            document.getElementById('message').textContent = data.error || 'Login failed';
            document.getElementById('message').style.color = 'red';
        }
    })
    .catch(error => {
        document.getElementById('message').textContent = 'An error occurred';
        document.getElementById('message').style.color = 'red';
    });
});

document.getElementById('forgotPasswordLink').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('forgotPasswordForm').style.display = 'block';
});

document.getElementById('forgotPasswordForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('resetEmail').value;

    fetch('/forgot-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById('message').textContent = data.message;
            document.getElementById('message').style.color = 'green';
        } else {
            document.getElementById('message').textContent = data.error || 'Password reset failed';
            document.getElementById('message').style.color = 'red';
        }
    })
    .catch(error => {
        document.getElementById('message').textContent = 'An error occurred';
        document.getElementById('message').style.color = 'red';
    });
});


