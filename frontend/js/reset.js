document.getElementById('forgotPasswordLink').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('resetPasswordForm').style.display = 'block';
});

document.getElementById('resetPasswordForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('resetEmail').value;

    fetch('/reset-password', {
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
