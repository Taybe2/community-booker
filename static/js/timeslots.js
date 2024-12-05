document.addEventListener('DOMContentLoaded', function () {
    const radioButtons = document.querySelectorAll('input[name="time_slot"]');
    const messageContainer = document.getElementById('message-container'); // Replace with your container's ID
    const form = document.getElementById('time-slot-form'); // Replace with your form's ID

    // Add change event listener to each radio button to clear the error message when a selection is made
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
            messageContainer.textContent = ""; // Clear the error message
            messageContainer.style.display = 'none';
        });
    });

    // Form submission handling
    form.addEventListener('submit', function (event) {
        const selectedTimeSlot = document.querySelector('input[name="time_slot"]:checked');
        if (!selectedTimeSlot) {
            event.preventDefault(); // Prevent form submission
            messageContainer.textContent = "Please select a time slot before submitting."; // Show the error message
            messageContainer.classList.add('error-message'); // Optional: Add a CSS class for styling
            messageContainer.style.display = 'block';
        }
    });
});
