const deleteModal = new bootstrap.Modal(document.getElementById("cancelBookingModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("confirmCancelButton");
const modalTitle = document.getElementById("cancelBookingModalLabel");
const modalContent = document.getElementById("cancelBookingModalText");

/*
 * Initializes deletion functionality for the provided delete(cancel booking) buttons.
 * 
 * For each button in the `deleteButtons` collection:
 * - Retrieves the associated booking's slug upon click or key press.
 * - Updates the `deleteConfirm` link's href to point to the 
 * deletion endpoint for the specific booking.
 * - Displays a confirmation modal (`deleteModal`) to prompt 
 * the user for confirmation before deletion.
 */
for (let button of deleteButtons) {
    // Handler function for click or keydown
    const openModal = (e) => {
        // Check for click or Enter key (keyCode 13 or key === 'Enter')
        if (e.type === "click" || (e.type === "keydown" && (e.key === "Enter" || e.keyCode === 13))) {
            e.preventDefault(); // Prevent default action for Enter key
            let bookingSlug = button.getAttribute("data-booking-slug");
            let bookingName = button.getAttribute("data-booking-name");
            let bookingDetails = button.getAttribute("data-booking-details")

            // Update the modal title and confirm button href
            modalTitle.textContent += `${bookingName}`
            modalContent.innerHTML = `Are you sure you want to cancel booking <strong>${bookingName}</strong> on <strong>${bookingDetails}</strong>? This action cannot be undone.`;
            deleteConfirm.href = `/booking/${bookingSlug}/cancel`;
            deleteModal.show();
        }
    };

    // Add event listeners for both click and keydown
    button.addEventListener("click", openModal);
    button.addEventListener("keydown", openModal);
}
