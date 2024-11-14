document.addEventListener('DOMContentLoaded', function() {
    // Get the JWT access token from local storage or wherever it's stored
    const accessToken = localStorage.getItem('access_token');  // Ensure the JWT is stored and accessible

    // Function to send the user's geolocation to the server
    function sendLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                fetch('/location/abc/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${accessToken}`  // Include the JWT token in the Authorization header
                    },
                    body: JSON.stringify({
                        lat: position.coords.latitude,
                        long: position.coords.longitude
                    })
                })
                .then(response => response.json())
                .then(data => console.log("Location sent:", data))
                .catch(error => console.error("Error sending location:", error));
            });
        } else {
            console.error('Geolocation is not supported by your browser');
        }
    }

    // Call sendLocation every 3 seconds (3000 milliseconds)
    setInterval(sendLocation, 3000);
});
