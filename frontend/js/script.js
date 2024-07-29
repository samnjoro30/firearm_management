document.addEventListener('DOMContentLoaded', () => {
    // Handle Police Officer Registration Form
    const registerPoliceForm = document.getElementById('registerPoliceForm');
    
    if (registerPoliceForm) {
        registerPoliceForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            const firstName = document.getElementById('firstName').value;
            const lastName = document.getElementById('lastName').value;
            const policeId = document.getElementById('policeId').value;
            const rankIndex = document.getElementById('rank').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;

            const response = await fetch('http://localhost:5000/register_police', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    firstName: firstName,
                    lastName: lastName,
                    policeId: policeId,
                    rank: rankIndex,
                    email: email,
                    phone: phone,
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
        });
    }

    // Handle Gun Registration Form
    const registerGunForm = document.getElementById('registerGunForm');
    if (registerGunForm) {
        registerGunForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            const serialNumber = document.getElementById('serialNumber').value;
            const gunType = document.getElementById('gunType').value;
            const manufacturerDate = document.getElementById('manufacturerDate').value;
            const gunStatus = document.getElementById('gunStatus').value;

            const response = await fetch('http://localhost/register_gun', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
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
        });
    }

    // Handle Gun Check-In Form
    const checkInGunForm = document.getElementById('checkInGunForm');
    if (checkInGunForm) {
        checkInGunForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            const serialNumber = document.getElementById('serialNumber').value;
            const policeOfficerId = document.getElementById('policeOfficerId').value;

            const response = await fetch('http://localhost:5000/backend/check_in_gun', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    serialNumber: serialNumber,
                    policeId: policeOfficerId,
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
        });
    }

    // Handle Gun Check-Out Form
    const checkOutGunForm = document.getElementById('checkOutGunForm');
    if (checkOutGunForm) {
        checkOutGunForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            const serialNumber = document.getElementById('serialNumber').value;
            const policeOfficerId = document.getElementById('policeOfficerId').value;

            const response = await fetch('http://localhost:5000/backend/check_out_gun', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    serialNumber: serialNumber,
                    policeId: policeOfficerId,
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
        });
    }

    // Fetch and display the list of police officers
    const policeListContainer = document.getElementById('policeList');
    if (policeListContainer) {
        async function fetchPoliceList() {
            const response = await fetch('http://localhost:5000/list_officers', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();

            if (response.ok) {
                data.forEach(officer => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${officer.firstName} ${officer.lastName} - ${officer.rank}`;
                    policeListContainer.appendChild(listItem);
                });
            } else {
                const messageElement = document.getElementById('message');
                messageElement.textContent = data.error || 'Failed to load police officers';
                messageElement.style.color = 'red';
            }
        }

        fetchPoliceList();
    }

    // Fetch and display the list of guns
    const gunListContainer = document.getElementById('gunList');
    if (gunListContainer) {
        async function fetchGunList() {
            const response = await fetch('http://localhost:5000/list_guns', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();

            if (response.ok) {
                data.forEach(gun => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${gun.serialNumber} - ${gun.gunType}`;
                    gunListContainer.appendChild(listItem);
                });
            } else {
                const messageElement = document.getElementById('message');
                messageElement.textContent = data.error || 'Failed to load guns';
                messageElement.style.color = 'red';
            }
        }

        fetchGunList();
    }
});
