// Open the confirmation modal dynamically
export function openConfirmationModal(modalTitle, modalText, buttonText, buttonUrl, hasConfirmation = false, confirmationValue = "") {
    // Conditionally render the confirmation section
    let modalBodyHtml = "";
    if (hasConfirmation) {
        modalBodyHtml = `
            <p>${modalText}</p>
            <p>Type the following to confirm:</p>
            <code>${confirmationValue}</code>
            <input type="text" class="form-control mt-3" required>
        `;
    } else {
        modalBodyHtml = `
            <p class="mb-0">${modalText}</p>
        `;
    }

    const modalHtml = `
        <div class="modal fade" id="confirmation-modal">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h4 class="modal-title">${modalTitle}</h4>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        ${modalBodyHtml}
                    </div>
                    <div class="modal-footer justify-content-between">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-danger">${buttonText}</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Append modal HTML to the body
    document.body.insertAdjacentHTML("beforeend", modalHtml);

    // Fetch the action button element
    var button = document.querySelector("#confirmation-modal .modal-footer .btn-danger");

    if (hasConfirmation) {
        // Fetch the input element
        var input = document.querySelector("#confirmation-modal .modal-body input");
        // Disable the button by default
        button.disabled = true;

        // Add an event listener to the input field to check text and enable button
        input.addEventListener("input", function() {
            if (input.value === confirmationValue) {
                button.disabled = false;
            } else {
                button.disabled = true;
            }
        });
    }

    // Show the modal
    $("#confirmation-modal").modal("show");

    // Handle the button click
    button.addEventListener("click", function() {
        if (!button.disabled) {
            window.location.href = buttonUrl;
        }
    });

    // Remove modal from DOM after it is closed
    $("#confirmation-modal").on("hidden.bs.modal", function() {
        $(this).remove();
    });
}

export function openDeleteConfirmationModal(itemType, deleteUrl, confirmationValue) {
    openConfirmationModal(
        `Delete ${itemType}`,
        `Are you sure you want to delete this ${itemType.toLowerCase()}?`,
        `Delete ${itemType}`,
        deleteUrl,
        true,
        confirmationValue
    );
}