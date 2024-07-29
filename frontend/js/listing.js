document.addEventListener('DOMContentLoaded', function() {
    fetchGuns();
    fetchPoliceOfficers();
});


function fetchGuns() {
    fetch('/api/list_guns')
        .then(response => response.json())
        .then(data => {
            const gunTable = document.getElementById('gun-table').getElementsByTagName('tbody')[0];
            data.forEach(gun => {
                let row = gunTable.insertRow();
                row.insertCell(0).innerText = gun.serialNumber;
                row.insertCell(1).innerText = gun.gunType;
                row.insertCell(2).innerText = gun.manufacturerDate;
                row.insertCell(3).innerText = gun.gunStatus;
            });
        })
        .catch(error => console.error('Error fetching guns:', error));
}

function fetchPoliceOfficers() {
    fetch('/api/list_officers')
        .then(response => response.json())
        .then(data => {
            console.log('Police officer data:', data); 
            const policeTable = document.getElementById('police-table').getElementsByTagName('tbody')[0];
            data.forEach(officer => {
                let row = policeTable.insertRow();
                row.insertCell(0).innerText = officer.policeId;
                row.insertCell(1).innerText = officer.firstName;
                row.insertCell(2).innerText = officer.lastName;
                row.insertCell(3).innerText = officer.rank;
                row.insertCell(4).innerText = officer.email;
                row.insertCell(5).innerText = officer.phonenumber
            });
        })
        .catch(error => console.error('Error fetching police officers:', error));
}
