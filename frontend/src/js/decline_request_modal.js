import { openConfirmationModal } from "./confirmation_modal.js";

// Attach the decline button with event listener
const requestDeclineButton = document.querySelector(".request-decline");
if (requestDeclineButton) {
    requestDeclineButton.addEventListener("click", function(event) {
        event.preventDefault();
        
        // Open the confirmation modal
        openConfirmationModal(
            "Decline Request",
            "Are you sure you want to decline this request?",
            "Decline Request",
            "",
            false,
        );
    });
}