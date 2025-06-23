if (window.location.pathname.toLowerCase().startsWith("/admin/jobs/logs")) {
    const logsContainer = document.querySelector(".job-logs table tbody");
    const scrollContainer = document.querySelector(".job-logs");
    const jobStatus = document.querySelector(".job-status");
    const jobDuration = document.querySelector(".job-duration");
    const jobFinishedAt = document.querySelector(".job-finished-at");

    if (logsContainer && scrollContainer && jobStatus && jobStatus.textContent.trim() === "Running") {
        const queryParams = new URLSearchParams(window.location.search);
        const jobId = queryParams.get("id");
        const jobRunId = queryParams.get("run_id");
        let offset = logsContainer.querySelectorAll("tr:not(.log-loading)").length;
        let polling = true;

        createLoadingRow();

        function createLoadingRow() {
            const existing = document.querySelector(".log-loading");
            if (existing) {
                logsContainer.appendChild(existing);
            } else {
                const loadingRow = document.createElement("tr");
                loadingRow.classList.add("log-loading");
                loadingRow.innerHTML = `
                    <td class="align-middle text-right text-muted" style="width: 5%"></td>
                    <td class="align-middle pl-2 text-muted">
                        <span class="loading-dots"></span>
                    </td>
                `;
                logsContainer.appendChild(loadingRow);
            }
        }

        function updateDetails(newStatus, data) {
            const statusHtml = {
                succeeded: `<span class="text-success"><i class="fas fa-check-circle"></i> Succeeded</span>`,
                failed: `<span class="text-danger"><i class="fas fa-times-circle"></i> Failed</span>`
            }[newStatus.toLowerCase()];

            if (statusHtml) {
                jobStatus.innerHTML = statusHtml;
            }

            if (data.duration && jobDuration) {
                jobDuration.style.display = "";
                const cell = jobDuration.querySelector("td:last-child");
                if (cell) cell.textContent = data.duration;
            }
            
            if (data.finished_at && jobFinishedAt) {
                jobFinishedAt.style.display = "";
                const cell = jobFinishedAt.querySelector("td:last-child");
                if (cell) cell.textContent = data.finished_at;
            }
        }

        function escapeHtml(str) {
            return str.replace(/[&<>"']/g, function (match) {
                const escapeMap = {
                    "&": "&amp;",
                    "<": "&lt;",
                    ">": "&gt;",
                    '"': "&quot;",
                    "'": "&#039;"
                };
                return escapeMap[match];
            });
        }

        function fetchLogs() {
            var urlParams = new URLSearchParams({ id: jobId, offset: offset });
            if (jobRunId) urlParams.set("run_id", jobRunId);

            fetch(`/admin/jobs/logs?${urlParams.toString()}`)
                .then(res => res.json())
                .then(data => {
                    if (data.logs && data.logs.length > 0) {
                        data.logs.forEach((log, index) => {
                            const row = document.createElement("tr");
                            row.innerHTML = `
                                <td class="align-middle text-right text-muted" style="width: 5%">
                                    ${offset + index + 1}
                                </td>
                                <td class="align-middle pl-2 log-${log.level.toLowerCase()}">
                                    ${log.created_at} - [ ${log.level} ] - ${escapeHtml(log.message)}
                                </td>
                            `;
                            logsContainer.appendChild(row);
                        });

                        offset += data.logs.length;
                        scrollContainer.scrollTop = scrollContainer.scrollHeight;
                    }

                    if (polling) {
                        createLoadingRow();
                    }

                    const newStatus = (data.status || "");
                    if (newStatus && newStatus !== "Running") {
                        updateDetails(newStatus, data);

                        const loadingRow = document.querySelector(".log-loading");
                        if (loadingRow) loadingRow.remove();

                        polling = false;
                    }
                });
        }

        const interval = setInterval(() => {
            if (polling) {
                fetchLogs();
            } else {
                clearInterval(interval);
            }
        }, 3000);
    }
}