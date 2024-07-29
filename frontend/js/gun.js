document.addEventListener('DOMContentLoaded', () => {
    const registerGunForm = document.getElementById('registerGunForm');
    if (registerGunForm) {
        registerGunForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            const serialNumber = document.getElementById('serialNumber').value;
            const gunType = document.getElementById('gunType').value;
            const manufacturerDate = document.getElementById('manufacturerDate').value;
            const gunStatus = document.getElementById('gunStatus').value;

            console.log('Sending data:', {
                serialNumber, gunType, manufacturerDate, gunStatus
            });

            try {
                const response = await fetch('http://localhost:5000/register_gun', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        serialNumber: serialNumber,
                        gunType: gunType,
                        manufacturerDate: manufacturerDate,
                        gunStatus: gunStatus
                    }),
                });

                const data = await response.json();
                console.log('Response:', data);

                const messageElement = document.getElementById('message');
                if (response.ok) {
                    messageElement.textContent = data.message || 'Registration successful';
                    messageElement.style.color = 'green';

                    setTimeout(()=> {
                        window.location.href='administration.html';
                    }, 1000);

                } else {
                    messageElement.textContent = data.error || 'An error occurred';
                    messageElement.style.color = 'red';
                }
            } catch (error) {
                const messageElement = document.getElementById('message');
                messageElement.textContent = 'An error occurred registering the gun';
                messageElement.style.color = 'red';
                console.error('Error:', error);
            }
        });
    } else {
        console.error('Form not found.');
    }
});
