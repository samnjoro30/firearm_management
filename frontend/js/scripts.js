document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const policeId = document.getElementById('policeId').value;
    
    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ policeId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('token', data.token);
            window.location.href = 'homepage.html';
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});

document.addEventListener('DOMContentLoaded', () => {
    // Handle Gun Registration Form
    const registerGunForm = document.getElementById('registerGunForm');
    if (registerGunForm) {
        registerGunForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            const serialNumber = document.getElementById('serialNumber').value;
            const gunType = document.getElementById('gunType').value;
            const manufacturerDate = document.getElementById('manufacturerDate').value;
            const gunStatus = document.getElementById('gunStatus').value;

            try {
                const response = await fetch('http://localhost/backend/register_gun', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}` // Make sure you store the token in local storage or a similar place
                    },
                    body: JSON.stringify({
                        serialNumber: serialNumber,
                        gunType: gunType,
                        manufacturerDate: manufacturerDate,
                        gunStatus: gunStatus,
                    }),
                });

                const data = await response.json();
                const messageElement = document.getElementById('message');

                if (response.ok) {
                    messageElement.textContent = data.message;
                    messageElement.style.color = 'green';
                } else {
                    messageElement.textContent = data.error || 'An error occurred';
                    messageElement.style.color = 'red';
                }
            } catch (error) {
                const messageElement = document.getElementById('message');
                messageElement.textContent = 'An error occurred while registering the gun';
                messageElement.style.color = 'red';
                console.error('Error:', error);
            }
        });
    }
});
