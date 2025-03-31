// Only run if we are on the frontend create request page
if (window.location.pathname.toLowerCase().startsWith("/requests/create")) {
    const environmentSelect = document.querySelector('select[name="environments"]');

    const nonprodPIDInput = document.querySelector('input[name="nonprod_pid"]');
    const prodPIDInput = document.querySelector('input[name="prod_pid"]');
    const scClearanceInputs = document.querySelectorAll('input[name="sc_clearance"]');

    const nonprodPIDGroup = nonprodPIDInput.closest(".form-group");
    const prodPIDGroup = prodPIDInput.closest(".form-group");
    const scClearanceGroup = scClearanceInputs[0]?.closest(".form-group");

    function updatePIDVisibility() {
        const selectedValues = Array.from(environmentSelect.selectedOptions).map(opt => opt.value);

        // Toggle Non-Prod PID
        if (selectedValues.includes("nonprod")) {
            nonprodPIDGroup.style.display = "block";
            nonprodPIDInput.setAttribute("required", "");
        } else {
            nonprodPIDGroup.style.display = "none";
            nonprodPIDInput.removeAttribute("required");
        }

        // Toggle Prod PID and SC Clearance
        if (selectedValues.includes("prod")) {
            prodPIDGroup.style.display = "block";
            prodPIDInput.setAttribute("required", "");
            scClearanceGroup.style.display = "block";
            scClearanceInputs.forEach(input => input.setAttribute("required", ""));
        } else {
            prodPIDGroup.style.display = "none";
            prodPIDInput.removeAttribute("required");
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