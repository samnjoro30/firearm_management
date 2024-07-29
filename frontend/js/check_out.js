document.addEventListener('DOMContentLoaded', () => {
    const checkOutGunForm = document.getElementById('checkOutGunForm');
    if (checkOutGunForm) {
        checkOutGunForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            const serialNumber = document.getElementById('serialNumber').value;
            const policeId = document.getElementById('policeId').value;

            try {
                const response = await fetch('http://localhost:5000/check_out', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}` // Ensure the token is included
                    },
                    body: JSON.stringify({
                        serialNumber: serialNumber,
                        policeId: policeId
                    }),
                });

                const data = await response.json();
                console.log('Response:', data);

                const messageElement = document.getElementById('message');
                if (response.ok) {
                    messageElement.textContent = data.success || "Check out successful";
                    messageElement.style.color = 'green';

                    // Redirect to administration.html after a short delay
                    setTimeout(() => {
                        window.location.href = 'administration.html';
                    }, 2000); // Delay of 2 seconds before redirecting
                } else {
                    messageElement.textContent = data.error || 'An error occurred';
                    messageElement.style.color = 'red';
                }
            } catch (error) {
                const messageElement = document.getElementById('message');
                messageElement.textContent = 'An error occurred while checking out the gun';
                messageElement.style.color = 'red';
                console.error('Error:', error);
            }
        });
    }
});
