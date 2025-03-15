// Map categories to Toastr types
const categoryMap = {
    success: "success",
    danger: "error",
    warning: "warning",
    info: "info"
};

// Toastr options
toastr.options = {
    closeButton: true,
    progressBar: true,
    positionClass: "toast-top-right",
    timeOut: "10000" // 10 seconds in milliseconds
};

// Get flash messages
const flashMessagesContainer = document.getElementById("flash-messages");
// Check the flash messages container exists as it might not if there are no messages
if (flashMessagesContainer) {
    const flashMessages = flashMessagesContainer.querySelectorAll(".flash-message");

    // Display each flash message as a Toastr notification
    flashMessages.forEach((flashMessage) => {
        const category = flashMessage.dataset.category; // Get message category
        const message = flashMessage.textContent.trim(); // Get message text
        const toastrType = categoryMap[category] || "info"; // Map category to Toastr type, default to 'info' if not found
        toastr[toastrType](message);
    });

    flashMessagesContainer.remove();
}