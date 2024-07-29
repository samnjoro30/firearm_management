document.addEventListener("DOMContentLoaded", function() {
    const registerPoliceForm = document.getElementById("registerPoliceForm");

    registerPoliceForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const firstName = document.getElementById("firstName").value;
        const lastName = document.getElementById("lastName").value;
        const policeId = document.getElementById("policeId").value;
        const rank = document.getElementById("rank").value;
        const email = document.getElementById("email").value;
        const phone = document.getElementById("phone").value;

        // Validate input
        if (!firstName || !lastName || !policeId || !rank || !email || !phone) {
            alert("All fields are required.");
            return;
        }

        // Validate email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert("Please enter a valid email address.");
            return;
        }

        // Send data to server
        fetch('http://localhost:5000/register_police', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ firstName, lastName, policeId, rank, email, phone })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
                registerPoliceForm.reset(); // Reset the form after successful submission
                // Optionally, redirect to another page or update UI
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("There was an error submitting the form. Please try again.");
        });
    });
});
document.getElementById('registerPoliceForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission

    const messageElement = document.getElementById('message');
    const processingMessage = document.createElement('p');
    processingMessage.classList.add('processing');
    processingMessage.textContent = 'Processing your request...';
    
    // Append the processing message to the form
    messageElement.innerHTML = ''; // Clear any previous messages
    messageElement.appendChild(processingMessage);

    // Simulate a delay for the processing (e.g., API call)
    setTimeout(() => {
        messageElement.innerHTML = ''; // Clear the processing message
        messageElement.textContent = 'Police registration successful!';
        messageElement.style.color = '#2ecc71'; // Change color on success
    }, 3000); // 3 seconds delay
});
