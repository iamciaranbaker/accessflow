// Attach event listener to all toggle-password buttons on the page
var togglePasswordButtons = document.querySelectorAll(".toggle-password");
if (togglePasswordButtons) {
    togglePasswordButtons.forEach(function(togglePasswordButton) {
        // Add a tooltip to the button
        togglePasswordButton.setAttribute("title", "Reveal " + togglePasswordButton.getAttribute("data-tooltip"));

        togglePasswordButton.addEventListener("click", function() {
            // Find the input associated with this button
            var inputGroup = togglePasswordButton.closest(".input-group");
            var input = inputGroup.querySelector("input");
            var icon = togglePasswordButton.querySelector("i");

            // Toggle the visibility of the password
            if (input.type === "password") {
                input.type = "text";
                icon.classList.remove("fa-eye");
                icon.classList.add("fa-eye-slash");
                togglePasswordButton.setAttribute("title", "Conceal " + togglePasswordButton.getAttribute("data-tooltip"));
            } else {
                input.type = "password";
                icon.classList.remove("fa-eye-slash");
                icon.classList.add("fa-eye");
                togglePasswordButton.setAttribute("title", "Reveal " + togglePasswordButton.getAttribute("data-tooltip"));
            }
        });
    });
}