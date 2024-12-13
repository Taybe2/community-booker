document.addEventListener('DOMContentLoaded', function () {
    // Select all radio buttons with the name "time_slot"
    const radioButtons = document.querySelectorAll('input[name="time_slot"]');

    // Reference the message container for displaying error messages
    const messageContainer = document.getElementById('message-container'); // Replace with your container's ID

    // Reference the form element to handle form submission
    const form = document.getElementById('time-slot-form'); // Replace with your form's ID

    /*
     * Add a 'change' event listener to each radio button.
     * This clears the error message whenever a radio button is selected.
     */
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
            messageContainer.textContent = ""; // Clear any error message
            messageContainer.style.display = 'none'; // Hide the message container
        });
    });

    /*
     * Add a 'submit' event listener to the form.
     * Validates that a time slot is selected before allowing submission.
     */
    form.addEventListener('submit', function (event) {
        // Check if a radio button is selected
        const selectedTimeSlot = document.querySelector('input[name="time_slot"]:checked');

        if (!selectedTimeSlot) {
            event.preventDefault(); // Prevent form submission if no time slot is selected

            // Display an error message in the message container
            messageContainer.textContent = "Please select a time slot before submitting.";
            messageContainer.classList.add('error-message'); // Add a CSS class for error styling (optional)
            messageContainer.style.display = 'block'; // Make the message visible
        }
    });

    /*
     * Add a 'keydown' event listener for the Enter key.
     * Allows users to select radio buttons by pressing Enter when focusing on their labels.
     */
    document.addEventListener('keydown', (event) => {
        // Check if the Enter key is pressed and the active element is a label
        if (event.key === 'Enter' && document.activeElement.tagName === 'LABEL') {
            const label = document.activeElement; // Get the currently focused label
            const inputId = label.getAttribute('for'); // Get the 'for' attribute to find the corresponding input
            const radioInput = document.getElementById(inputId); // Find the input element with the matching ID

            // If the radio input exists and is not disabled, select it
            if (radioInput && !radioInput.disabled) {
                radioInput.checked = true; // Mark the radio button as selected
                
                // Trigger a 'change' event to clear any error messages
                radioInput.dispatchEvent(new Event('change', { bubbles: true }));
            }

            // Prevent the default Enter key behavior to avoid unexpected actions
            event.preventDefault();
        }
    });
});
