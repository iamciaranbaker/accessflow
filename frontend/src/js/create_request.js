// Only run if we are on the frontend create request page
if (window.location.pathname.toLowerCase().startsWith("/requests/create")) {
    const environmentCheckboxes = document.querySelectorAll('input[name="environments"]');

    const nonprodPIDGroup = document.querySelector('input[name="nonprod_pid"]').closest('.form-group');
    const prodPIDGroup = document.querySelector('input[name="prod_pid"]').closest('.form-group');
    const scClearanceGroup = document.querySelector('input[name="sc_clearance"]').closest('.form-group');

    function updatePIDVisibility() {
        const selectedValues = Array.from(environmentCheckboxes).filter(cb => cb.checked).map(cb => cb.value);

        // Show/hide based on selected checkboxes
        nonprodPIDGroup.style.display = selectedValues.includes("nonprod") ? "block" : "none";
        prodPIDGroup.style.display = selectedValues.includes("prod") ? "block" : "none";
        scClearanceGroup.style.display = selectedValues.includes("prod") ? "block" : "none";
    }

    // Initial state on page load
    updatePIDVisibility();

    // Attach event listener to each checkbox
    environmentCheckboxes.forEach(cb => {
        cb.addEventListener("change", updatePIDVisibility);
    });

    // Activate Select2
    $(".select2").select2();
}