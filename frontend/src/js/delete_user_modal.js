import { openDeleteConfirmationModal } from "./confirmation_modal.js";

// Attach the delete button with event listener in the user list
var userDeleteButtons = document.querySelectorAll(".user-delete");
if (userDeleteButtons) {
    userDeleteButtons.forEach(function(deleteButton) {
        deleteButton.addEventListener("click", function(event) {
            var userRow = event.target.closest("tr");
            var userId = userRow.getAttribute("data-user-id");
            var userEmailAddress = userRow.getAttribute("data-user-email-address");
            
            // Open the confirmation modal for user deletion
            openDeleteConfirmationModal("User", `/admin/users/delete?id=${userId}`, userEmailAddress);
        });
    });
}