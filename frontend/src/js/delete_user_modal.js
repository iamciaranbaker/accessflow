// Open the modal and set up the delete button link
function openDeleteModal(userId, userEmail) {
    var emailAddressText = document.getElementById("confirm-email-address");
    var emailAddressInput = document.getElementById("confirm-email-address-input");
    var deleteButton = document.getElementById("delete-user-btn");

    emailAddressText.innerHTML = userEmail;
    
    // Set the delete button"s data attribute to store the redirect URL
    deleteButton.setAttribute("data-url", "/admin/users/" + userId + "/delete");

    // Reset the email input and disable the delete button
    emailAddressInput.value = "";
    deleteButton.disabled = true;

    // Add an event listener to the input field to check email and enable button
    emailAddressInput.addEventListener("input", function() {
        if (emailAddressInput.value === userEmail) {
            deleteButton.disabled = false;
        } else {
            deleteButton.disabled = true;
        }
    });

    // Show the modal
    $("#delete-user-modal").modal("show");
}

// Attach the delete button with event listener in the user list
var userDeleteBtn = document.querySelectorAll(".user-delete");
if (userDeleteBtn) {
    userDeleteBtn.forEach(function(deleteButton) {
        deleteButton.addEventListener("click", function(event) {
            var userRow = event.target.closest("tr");
            var userId = userRow.getAttribute("data-user-id");
            var userEmail = userRow.querySelector(".user-email-address").textContent.trim();
            
            openDeleteModal(userId, userEmail);
        });
    });
}

// Handle delete button click and redirect
var deleteUserBtn = document.getElementById("delete-user-btn");
if (deleteUserBtn) {
    deleteUserBtn.addEventListener("click", function() {
        if (!this.disabled) {
            // Redirect to the delete URL
            window.location.href = this.getAttribute("data-url");
        }
    });
}