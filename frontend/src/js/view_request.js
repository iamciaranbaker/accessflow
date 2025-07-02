// Only run if we are on the view request page
if (window.location.pathname.toLowerCase().startsWith("/admin/requests")) {
    const nonprodRadios = document.querySelectorAll('input[type="radio"][name="selected_pid_nonprod"]');
    const prodRadios = document.querySelectorAll('input[type="radio"][name="selected_pid_prod"]');
    const hostGroupTable = document.getElementById("host-group-matches");
    const pidTable = document.getElementById("pid-matches");

    function getEnvTypeFromName(name) {
        return name.includes("nonprod") ? "nonprod" : "prod";
    }

    function getPidNameFromRow(radio) {
        const row = radio.closest("tr");
        const nameCell = row?.querySelector("td .d-block");
        return nameCell ? nameCell.textContent.trim() : null;
    }

    function createWarningElement(type, message, icon = "exclamation-triangle") {
        const wrapper = document.createElement("div");
        wrapper.className = `row warning-box ${type}`;
        wrapper.innerHTML = `
            <div class="col-12">
                <div class="alert alert-warning">
                    <i class="icon fas fa-${icon}"></i> ${message}
                </div>
            </div>
        `;
        return wrapper;
    }

    function checkPidNameMismatch() {
        const nonprodRadio = document.querySelector('input[name="selected_pid_nonprod"]:checked');
        const prodRadio = document.querySelector('input[name="selected_pid_prod"]:checked');
        const container = document.querySelector(".content .container-fluid");
        const existing = container.querySelector(".pid-name-mismatch");
    
        if (nonprodRadio && prodRadio) {
            const name1 = getPidNameFromRow(nonprodRadio);
            const name2 = getPidNameFromRow(prodRadio);
    
            if (name1 && name2 && name1 !== name2) {
                if (!existing) {
                    const warning = createWarningElement(
                        "pid-name-mismatch",
                        "The selected Non-Production PID and Production PID have different names. Are you sure they're the same person?"
                    );
                    container.prepend(warning);
                }
            } else {
                existing?.remove();
            }
        } else {
            existing?.remove();
        }
    }
    
    function checkConfidenceWarnings() {
        const container = document.querySelector(".content .container-fluid");
    
        // Remove existing confidence warnings (nonprod and prod)
        container.querySelectorAll(".confidence-warning-nonprod, .confidence-warning-prod").forEach(el => el.remove());
    
        const warnings = [];
    
        ["nonprod", "prod"].forEach(envType => {
            const radio = document.querySelector(`input[name="selected_pid_${envType}"]:checked`);
            if (radio) {
                const row = radio.closest("tr");
                const confidenceCell = row?.querySelectorAll("td")[3];
                const confidenceText = confidenceCell?.textContent?.trim().replace("%", "");
                const confidence = parseInt(confidenceText, 10);
    
                // Anything below 85% is either amber or red
                if (!isNaN(confidence) && confidence < 85) {
                    const warning = createWarningElement(
                        `confidence-warning-${envType}`,
                        `The selected ${envType === "nonprod" ? "Non-Production" : "Production"} PID has a confidence rating below 85%. Are you sure this is the correct person?`
                    );
                    // Push in the order of nonprod -> prod because of loop order
                    warnings.push(warning);
                }
            }
        });
    
        // Insert in order: first one added will show on top
        warnings.reverse().forEach(warning => {
            container.prepend(warning);
        });
    }

    function updateVisibility(selectedPid, envType) {
        if (!hostGroupTable) return;
    
        const rows = hostGroupTable.querySelectorAll("tbody tr");
    
        rows.forEach(row => {
            const badge = row.querySelector("span.badge");
            if (!badge) return;
    
            const rowType = badge.classList.contains("bg-success") ? "nonprod" :
                            badge.classList.contains("bg-danger") ? "prod" : null;
    
            if (rowType !== envType) return;
    
            // Find columns
            const tdList = row.querySelectorAll("td");
            const envCol = tdList[2];
            const hostCol = tdList[3];
    
            let envVisible = false;
            let hostVisible = false;
    
            // Update visibility and count in Environments column
            envCol.querySelectorAll("code[data-pid-id]").forEach(code => {
                const show = code.getAttribute("data-pid-id") === selectedPid;
                code.style.display = show ? "inline-block" : "none";
                if (show) envVisible = true;
            });
    
            // Update visibility and count in Host Groups column
            hostCol.querySelectorAll("code[data-pid-id]").forEach(code => {
                const show = code.getAttribute("data-pid-id") === selectedPid;
                code.style.display = show ? "inline-block" : "none";
                if (show) hostVisible = true;
            });
    
            // Hide row if EITHER environments or host groups are missing
            row.style.display = (envVisible && hostVisible) ? "" : "none";
        });
    }    

    function handleRadioChange(radio) {
        const envType = getEnvTypeFromName(radio.name);
        updateVisibility(radio.value, envType);
        checkPidNameMismatch();
        checkConfidenceWarnings();
    }

    function openApprovalSummaryModal(approveUrl) {
        const nonprodRadio = document.querySelector('input[name="selected_pid_nonprod"]:checked');
        const prodRadio = document.querySelector('input[name="selected_pid_prod"]:checked');
    
        const visibleEnvRows = Array.from(document.querySelectorAll("#host-group-matches tbody tr"))
            .filter(row => getComputedStyle(row).display !== "none");
    
        function getPidMeta(radio) {
            const row = radio.closest("tr");
            const name = row.querySelector(".d-block")?.textContent.trim() || "Unknown";
            const pid = row.querySelector(".small")?.textContent.trim() || "Unknown";
            const team = row.querySelectorAll("td")[1]?.textContent.trim() || "-";
            const confidence = row.querySelectorAll("td")[3]?.textContent.trim() || "-";
            return { name, pid, team, confidence };
        }
    
        function generateSection(envType, radio) {
            if (!radio) return "";
    
            const { name, pid, team, confidence } = getPidMeta(radio);
            const titleColor = envType === "nonprod" ? "success" : "danger";
            const heading = envType === "nonprod" ? "Non-Production" : "Production";
    
            const matchingRows = visibleEnvRows.filter(row => {
                const badge = row.querySelector("span.badge");
                return badge && badge.classList.contains(`bg-${titleColor}`);
            });
    
            const cards = matchingRows.map(row => {
                const cells = row.querySelectorAll("td");
                const service = cells[0]?.textContent.trim();
            
                const environments = Array.from(cells[2]?.querySelectorAll("code"))
                    .filter(code => code.style.display !== "none")
                    .map(code => `<code class="mr-1">${code.textContent}</code>`)
                    .join("") || "<em>None</em>";
            
                const hostGroups = Array.from(cells[3]?.querySelectorAll("code"))
                    .filter(code => code.style.display !== "none")
                    .map(code => `<code class="mr-1">${code.textContent}</code>`)
                    .join("") || "<em>None</em>";
            
                return `
                    <div class="service-card border rounded p-3 mb-3 shadow-sm">
                        <table class="table table-sm table-borderless mb-0">
                            <tbody>
                                <tr>
                                    <td class="align-middle font-weight-bold" width="20%">Service</td>
                                    <td class="align-middle" width="80%">${service}</td>
                                <tr>
                                    <td class="align-middle font-weight-bold" width="20%">Environments</td>
                                    <td class="align-middle" width="80%">${environments}</td>
                                </tr>
                                <tr>
                                    <td class="align-middle font-weight-bold" width="20%">Host Groups</td>
                                    <td class="align-middle" width="80%">${hostGroups}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                `;
            }).join("");
    
            return `
                <section class="mb-4">
                    <div class="border-start border-${titleColor} ps-3 mb-3">
                        <div class="service-card border rounded p-3 mb-3 bg-light shadow-sm">
                            <table class="table table-sm table-borderless mb-0">
                                <tbody>
                                    <tr>
                                        <td class="align-middle font-weight-bold" width="20%">PID</td>
                                        <td class="align-middle" width="80%">${pid}</td>
                                    </tr>
                                    <tr>
                                        <td class="align-middle font-weight-bold" width="20%">Name</td>
                                        <td class="align-middle" width="80%">${name}</td>
                                    </tr>
                                    <tr>
                                        <td class="align-middle font-weight-bold" width="20%">Team</td>
                                        <td class="align-middle" width="80%">${team}</td>
                                    </tr>
                                    <tr>
                                        <td class="align-middle font-weight-bold" width="20%">Environment Type</td>
                                        <td class="align-middle" width="80%">
                                            <span class="badge bg-${titleColor}">
                                                ${heading}
                                            </span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="offset-1">
                        ${cards || "<p class='text-muted'><em>No applicable services for this PID.</em></p>"}
                    </div>
                </section>
            `;
        }
    
        const modalHtml = `
            <div class="modal fade" id="approve-request-modal">
                <div class="modal-dialog modal-xl">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h4 class="modal-title">Approve Request </h4>
                            <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body overflow-auto pb-0" style="max-height: 70vh;">
                            <p>Are you sure you want to approve this request?</p>
                            <p>By approving this request, you will grant the following access:</p>
                            ${generateSection("nonprod", nonprodRadio)}
                            ${generateSection("prod", prodRadio)}
                        </div>
                        <div class="modal-footer justify-content-between">
                            <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-success">Approve Request</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    
        document.body.insertAdjacentHTML("beforeend", modalHtml);
        $("#approve-request-modal").modal("show");
    
        document.querySelector("#approve-request-modal .btn-success").addEventListener("click", function () {
            window.location.href = approveUrl;
        });
    
        $("#approve-request-modal").on("hidden.bs.modal", function () {
            $(this).remove();
        });
    }
      

    // Initial setup on load
    [...nonprodRadios, ...prodRadios].forEach(radio => {
        if (radio.checked) handleRadioChange(radio);
        radio.addEventListener("change", function () {
            if (this.checked) handleRadioChange(this);
        });
    });

    // Enable row clicking in the PID match table
    if (pidTable) {
        pidTable.querySelectorAll("tbody tr").forEach(row => {
            row.addEventListener("click", function () {
                const radio = this.querySelector('input[type="radio"]');
                if (radio && !radio.checked) {
                    radio.checked = true;
                    radio.dispatchEvent(new Event("change"));
                }
            });
        });
    }

    document.getElementById("request-approve").addEventListener("click", function (e) {
        e.preventDefault();
        openApprovalSummaryModal("/admin/requests/edit?id=1");
    });
}