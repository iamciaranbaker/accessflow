import { openDeleteConfirmationModal } from "./confirmation_modal.js";

// Attach the delete button with event listener in the service list
var serviceDeleteButtons = document.querySelectorAll(".service-delete");
if (serviceDeleteButtons) {
    serviceDeleteButtons.forEach(function(deleteButton) {
        deleteButton.addEventListener("click", function(event) {
            var serviceRow = event.target.closest("tr");
            var serviceId = serviceRow.getAttribute("data-service-id");
            var serviceName = serviceRow.getAttribute("data-service-name");
            
            // Open the confirmation modal for service deletion
            openDeleteConfirmationModal("Service", `/admin/services/delete?service_id=${serviceId}`, serviceName);
        });
    });
}