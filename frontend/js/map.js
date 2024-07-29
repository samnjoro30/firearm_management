document.addEventListener('DOMContentLoaded', function() {
    const map = L.map('map').setView([0, 0], 2); // Initialize map at the center of the world with zoom level 2

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    fetchGuns(map);
});

function fetchGuns(map) {
    fetch('http://localhost:5000/list_guns')
        .then(response => response.json())
        .then(data => {
            data.forEach(gun => {
                if (gun.latitude && gun.longitude) {
                    L.marker([gun.latitude, gun.longitude])
                        .addTo(map)
                        .bindPopup(`<b>Serial Number:</b> ${gun.serialNumber}<br><b>Type:</b> ${gun.gunType}<br><b>Status:</b> ${gun.gunStatus}`);
                }
            });
        })
        .catch(error => console.error('Error fetching guns:', error));
}
