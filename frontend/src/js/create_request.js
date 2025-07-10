// Only run if we are on the frontend create request page
if (window.location.pathname.toLowerCase().startsWith("/requests/create")) {
    const queryParams = new URLSearchParams(window.location.search);
    const requestType = queryParams.get("type");

    if (queryParams && requestType && (requestType == "account_creation" || requestType == "service_access")) {
        const environmentSelect = document.querySelector('select[name="environments"]');

        const nonProdPIDInput = document.querySelector('input[name="nonprod_pid"]');
        const nonProdSSHKeyInput = document.querySelector('textarea[name="nonprod_ssh_key"]');
        const prodPIDInput = document.querySelector('input[name="prod_pid"]');
        const prodSSHKeyInput = document.querySelector('textarea[name="prod_ssh_key"]');
        const scClearanceInputs = document.querySelectorAll('input[name="sc_clearance"]');

        const nonProdPIDGroup = nonProdPIDInput.closest(".form-group");
        const prodPIDGroup = prodPIDInput.closest(".form-group");
        const scClearanceGroup = scClearanceInputs[0]?.closest(".form-group");
        if (requestType == "account_creation" && nonProdSSHKeyInput) var nonProdSSHKeyGroup = nonProdSSHKeyInput.closest(".form-group");
        if (requestType == "account_creation" && prodSSHKeyInput) var prodSSHKeyGroup = prodSSHKeyInput.closest(".form-group");

        // Store original min/max values so we can restore them later
        const nonProdMin = nonProdPIDInput.getAttribute("minlength");
        const nonProdMax = nonProdPIDInput.getAttribute("maxlength");
        const prodMin = prodPIDInput.getAttribute("minlength");
        const prodMax = prodPIDInput.getAttribute("maxlength");

        // Activate Select2
        $(".select2").select2();

        function updateEnvironmentVisibility() {
            const selectedValues = Array.from(environmentSelect.selectedOptions).map(opt => opt.value);

            // Toggle Non-Prod PID
            if (selectedValues.includes("nonprod")) {
                nonProdPIDGroup.style.display = "block";
                nonProdPIDInput.setAttribute("required", "");
                nonProdPIDInput.setAttribute("minlength", nonProdMin);
                nonProdPIDInput.setAttribute("maxlength", nonProdMax);

                if (requestType == "account_creation") {
                    nonProdSSHKeyGroup.style.display = "block";
                    nonProdPIDInput.setAttribute("required", "");
                }
            } else {
                nonProdPIDGroup.style.display = "none";
                nonProdPIDInput.removeAttribute("required");
                nonProdPIDInput.removeAttribute("minlength");
                nonProdPIDInput.removeAttribute("maxlength");

                if (requestType == "account_creation") {
                    nonProdSSHKeyGroup.style.display = "none";
                    nonProdPIDInput.removeAttribute("required");
                }
            }

            // Toggle Prod PID and SC Clearance
            if (selectedValues.includes("prod")) {
                prodPIDGroup.style.display = "block";
                prodPIDInput.setAttribute("required", "");
                prodPIDInput.setAttribute("minlength", prodMin);
                prodPIDInput.setAttribute("maxlength", prodMax);

                if (requestType == "account_creation") {
                    prodSSHKeyGroup.style.display = "block";
                    prodPIDInput.setAttribute("required", "");
                }

                scClearanceGroup.style.display = "block";
                scClearanceInputs.forEach(input => input.setAttribute("required", ""));
            } else {
                prodPIDGroup.style.display = "none";
                prodPIDInput.removeAttribute("required");
                prodPIDInput.removeAttribute("minlength");
                prodPIDInput.removeAttribute("maxlength");

                if (requestType == "account_creation") {
                    prodSSHKeyGroup.style.display = "none";
                    prodPIDInput.removeAttribute("required");
                }

                scClearanceGroup.style.display = "none";
                scClearanceInputs.forEach(input => input.removeAttribute("required"));
            }
        }

        // Initial state on page load
        updateEnvironmentVisibility();

        // Attach change event to select element
        $(environmentSelect).on("change", updateEnvironmentVisibility);
    }
}