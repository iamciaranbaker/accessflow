// Only run if we are on the frontend create request page
if (window.location.pathname.toLowerCase().startsWith("/requests/create")) {
    const environmentSelect = document.querySelector('select[name="environments"]');

    const nonprodPIDInput = document.querySelector('input[name="nonprod_pid"]');
    const prodPIDInput = document.querySelector('input[name="prod_pid"]');
    const scClearanceInputs = document.querySelectorAll('input[name="sc_clearance"]');

    const nonprodPIDGroup = nonprodPIDInput.closest(".form-group");
    const prodPIDGroup = prodPIDInput.closest(".form-group");
    const scClearanceGroup = scClearanceInputs[0]?.closest(".form-group");

    // Store original min/max values so we can restore them later
    const nonprodMin = nonprodPIDInput.getAttribute("minlength");
    const nonprodMax = nonprodPIDInput.getAttribute("maxlength");
    const prodMin = prodPIDInput.getAttribute("minlength");
    const prodMax = prodPIDInput.getAttribute("maxlength");

    function updatePIDVisibility() {
        const selectedValues = Array.from(environmentSelect.selectedOptions).map(opt => opt.value);

        // Toggle Non-Prod PID
        if (selectedValues.includes("nonprod")) {
            nonprodPIDGroup.style.display = "block";
            nonprodPIDInput.setAttribute("required", "");
            nonprodPIDInput.setAttribute("minlength", nonprodMin);
            nonprodPIDInput.setAttribute("maxlength", nonprodMax);
        } else {
            nonprodPIDGroup.style.display = "none";
            nonprodPIDInput.removeAttribute("required");
            nonprodPIDInput.removeAttribute("minlength");
            nonprodPIDInput.removeAttribute("maxlength");
        }

        // Toggle Prod PID and SC Clearance
        if (selectedValues.includes("prod")) {
            prodPIDGroup.style.display = "block";
            prodPIDInput.setAttribute("required", "");
            prodPIDInput.setAttribute("minlength", prodMin);
            prodPIDInput.setAttribute("maxlength", prodMax);

            scClearanceGroup.style.display = "block";
            scClearanceInputs.forEach(input => input.setAttribute("required", ""));
        } else {
            prodPIDGroup.style.display = "none";
            prodPIDInput.removeAttribute("required");
            prodPIDInput.removeAttribute("minlength");
            prodPIDInput.removeAttribute("maxlength");

            scClearanceGroup.style.display = "none";
            scClearanceInputs.forEach(input => input.removeAttribute("required"));
        }
    }

    // Initial state on page load
    updatePIDVisibility();

    // Attach change event to select element
    $(environmentSelect).on("change", updatePIDVisibility);

    // Activate Select2
    $(".select2").select2();
}
