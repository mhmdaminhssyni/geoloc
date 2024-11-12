document.addEventListener('DOMContentLoaded', function() {
    // Define a function to send geolocation data to the server
    function sendGeolocationData() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                fetch('/location/abc/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: new URLSearchParams({
                        lat: position.coords.latitude,
                        long: position.coords.longitude
                    })
                })
                .then(response => response.json())
                .then(data => console.log(data.status || data.error))  // Log the response instead of alerting to avoid interruptions
                .catch(error => console.error('Error:', error));
            });
        } else {
            console.error('Geolocation is not supported by your browser');
        }
    }

    // Call the function every 3 seconds (3000 milliseconds)
    setInterval(sendGeolocationData, 3000);
});
