console.log("hello")
const deleteModal = new bootstrap.Modal(document.getElementById("cancelBookingModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("confirmCancelButton");

/*
 * Initializes deletion functionality for the provided delete(cancel booking) buttons.
 * 
 * For each button in the `deleteButtons` collection:
 * - Retrieves the associated booking's slug upon click.
 * - Updates the `deleteConfirm` link's href to point to the 
 * deletion endpoint for the specific booking.
 * - Displays a confirmation modal (`deleteModal`) to prompt 
 * the user for confirmation before deletion.
 */
for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
        let bookingSlug = e.target.getAttribute("data-booking-slug");
        deleteConfirm.href = `/booking/${bookingSlug}/cancel`;
        deleteModal.show();
    });
}