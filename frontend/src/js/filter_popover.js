function openFilterPopover(element, filters = []) {
    // Remove existing popover
    $(element).popover("dispose");

    // Build popover content
    let filterFieldsHtml = "";
    filters.forEach(filter => {
        filterFieldsHtml += `
            <div class="form-group mb-1">
                <label class="col-form-label" for="${filter.name}">${filter.label}</label>
                <select name="${filter.name}" class="form-control form-control-sm select2" multiple>
                    ${filter.options.map(option => `
                        <option value="${option.value}">${option.label}</option>
                    `).join('')}
                </select>
            </div>
        `;
    });
    const popoverHtml = `
        <div>
            <form style="min-width: 250px">
                ${filterFieldsHtml}
                <button type="submit" class="btn btn-primary btn-sm btn-block mt-3">Apply Filter(s)</button>
            </form>
        </div>
    `;

    // Initialize popover
    $(element).popover({
        html: true,
        content: popoverHtml,
        title: "Apply Filter(s)",
        placement: "bottom",
        container: "body",
        trigger: "manual",
        animation: true,
        sanitize: false
    });

    // Show popover
    $(element).popover("show");

    // After popover is shown, initialize Select2 and event listeners
    const popoverId = element.getAttribute("aria-describedby");
    const popover = document.getElementById(popoverId);

    if (!popover) return;

    const $popover = $("#" + popoverId);
    const $form = $popover.find("form");
    const urlParams = new URLSearchParams(window.location.search);

    // Pre-select values based on URL params
    filters.forEach(filter => {
        const selectedValues = urlParams.getAll(`filter[${filter.name}]`);
        const $select = $popover.find(`select[name="${filter.name}"]`);

        $select.find("option").each(function() {
            if (selectedValues.includes(this.value)) {
                $(this).prop("selected", true);
            }
        });

        // Initialize Select2 on live DOM element, point dropdownParent to popover
        $select.select2({
            dropdownParent: $popover,
            closeOnSelect: true,
            theme: "bootstrap4"
        });
    });

    // Add form submit listener
    $form.on("submit", function(event) {
        event.preventDefault();

        const data = new FormData(this);
        const newParams = new URLSearchParams();

        // Preserve existing non-filter params, excluding "page"
        const currentParams = new URLSearchParams(window.location.search);
        for (const [key, value] of currentParams.entries()) {
            if (!key.startsWith("filter[") && key !== "page") {
                newParams.append(key, value);
            }
        }

        // Add filters
        for (const [key, value] of data.entries()) {
            if (value.trim()) {
                newParams.append(`filter[${key}]`, value.trim());
            }
        }

        // Build redirect URL
        const queryString = newParams.toString();
        if (queryString) {
            window.location.href = `${window.location.pathname}?${queryString}`;
        } else {
            window.location.href = window.location.pathname;
        }
    });

    // Close popover if clicking outside
    function handleClickOutside(event) {
        if (!popover.contains(event.target) && !element.contains(event.target)) {
            $(element).popover("hide");
            document.removeEventListener("mousedown", handleClickOutside);
        }
    }

    setTimeout(() => {
        document.addEventListener("mousedown", handleClickOutside);
    }, 0);

    $(element).on("hidden.bs.popover", function() {
        $(element).popover("dispose");
    });
}

const filterButton = document.querySelector(".filter");
if (filterButton) {
    filterButton.addEventListener("click", function(event) {
        event.preventDefault();
        openFilterPopover(this, filterOptions);
    });
}