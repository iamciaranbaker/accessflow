document.addEventListener("DOMContentLoaded", function() {
    // Attach event listener to all toggle-password buttons on the page.
    var toggleButtons = document.querySelectorAll(".toggle-password");

    toggleButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            // Find the input associated with this button.
            var inputGroup = button.closest(".input-group");
            var input = inputGroup.querySelector("input");
            var icon = button.querySelector("i");

            // Toggle the visibility of the password.
            if (input.type === "password") {
                input.type = "text";
                icon.classList.remove("fa-eye");
                icon.classList.add("fa-eye-slash");
                button.setAttribute("title", "Conceal Password");
            } else {
                input.type = "password";
                icon.classList.remove("fa-eye-slash");
                icon.classList.add("fa-eye");
                button.setAttribute("title", "Reveal Password");
            }
        });
    });
});