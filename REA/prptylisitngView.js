// Assuming each property listing has a unique ID
const propertyId = '123';

// Increment view count when the page loads
document.addEventListener('DOMContentLoaded', () => {
    incrementViewCount(propertyId);
});

function incrementViewCount(propertyId) {
    // Make a request to the server to increment the view count for the specified property ID
    // Example: Send a POST request to '/increment-view' endpoint with the property ID
    fetch('/increment-view', {
        method: 'POST',
        body: JSON.stringify({ propertyId }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to increment view count');
        }
        // View count successfully updated
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
