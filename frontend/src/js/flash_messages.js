document.addEventListener("DOMContentLoaded", function () {
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
        timeOut: "10000" // Duration in milliseconds
    };

    // Get flash messages
    const flashMessagesContainer = document.getElementById("flash-messages");
    if (!flashMessagesContainer) return; // Exit if no flash messages container

    const flashMessages = flashMessagesContainer.querySelectorAll(".flash-message");

    // Display each flash message as a Toastr notification
    flashMessages.forEach((flashMessage) => {
        const category = flashMessage.dataset.category; // Get category
        const message = flashMessage.textContent.trim(); // Get message text
        const toastrType = categoryMap[category] || "info"; // Map category to Toastr type
        toastr[toastrType](message);
    });
});