// Example: A function to show an alert when the user clicks a button
function myFunction() {
    alert("Booking Confirmed!");
}

// Example: Form validation for booking form (Passenger details)
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        const name = document.querySelector('#passenger_name').value;
        const email = document.querySelector('#passenger_email').value;
        const address = document.querySelector('#passenger_address').value;

        if (!name || !email || !address) {
            alert("Please fill in all the details.");
            event.preventDefault(); // Prevent form submission
        }
    });
});

// Example: Smooth scroll to section when a button is clicked
document.querySelector('.scroll-btn').addEventListener('click', function() {
    document.querySelector('#target-section').scrollIntoView({
        behavior: 'smooth'
    });
});
