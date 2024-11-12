document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('geolocationForm').addEventListener('submit', function(e) {
        e.preventDefault();

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
                .then(data => alert(data.status || data.error))
                .catch(error => console.error('Error:', error));
            });
        } else {
            alert('Geolocation is not supported by your browser');
        }
    });
});
