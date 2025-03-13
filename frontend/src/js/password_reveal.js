// Attach event listener to all toggle-password buttons on the page
var toggleButtons = document.querySelectorAll(".toggle-password");

toggleButtons.forEach(function(button) {
    // Add a tooltip to the button
    button.setAttribute("title", "Reveal " + button.getAttribute("data-tooltip"));

    button.addEventListener("click", function() {
        // Find the input associated with this button
        var inputGroup = button.closest(".input-group");
        var input = inputGroup.querySelector("input");
        var icon = button.querySelector("i");

        // Toggle the visibility of the password
        if (input.type === "password") {
            input.type = "text";
            icon.classList.remove("fa-eye");
            icon.classList.add("fa-eye-slash");
            button.setAttribute("title", "Conceal " + button.getAttribute("data-tooltip"));
        } else {
            input.type = "password";
            icon.classList.remove("fa-eye-slash");
            icon.classList.add("fa-eye");
            button.setAttribute("title", "Reveal " + button.getAttribute("data-tooltip"));
        }
    });
});