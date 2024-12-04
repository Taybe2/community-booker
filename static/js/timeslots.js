document.addEventListener('DOMContentLoaded', function () {
    const radioButtons = document.querySelectorAll('input[name="time_slot"]');
    const submitButton = document.getElementsByClassName('submit-button')[0];
    
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
            submitButton.disabled = !document.querySelector('input[name="time_slot"]:checked').checked;
        });
    });
});