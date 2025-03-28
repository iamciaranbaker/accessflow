function openGoToPagePopover(element) {
    // Remove any existing popover
    $(element).popover("dispose");

    const page = element.getAttribute("data-page");
    const pageMax = element.getAttribute("data-page-max");

    const popoverHtml = `
        <div class="input-group">
            <input type="number" class="form-control" id="pageNumberInput" min="1" max="${pageMax}" value="${page}" step="1">
            <div class="input-group-append">
                <button class="btn btn-default" type="button" id="paginate-page-plus">
                    <i class="fas fa-plus"></i>
                </button>
                <button class="btn btn-default" type="button" id="paginate-page-minus">
                    <i class="fas fa-minus"></i>
                </button>
            </div>
        </div>
        <button class="btn btn-primary btn-sm mt-2" id="paginate-page-go">Go</button>
    `;

    // Initialize popover
    $(element).popover({
        html: true,
        content: popoverHtml,
        title: "Go To Page",
        placement: "top",
        container: "body",
        trigger: "manual",
        animation: true,
        sanitize: false
    });
    // Show the popover
    $(element).popover("show");

    // After popover is shown, attach logic
    const popoverId = element.getAttribute("aria-describedby");
    const popover = document.getElementById(popoverId);

    if (!popover) return;

    const pageInput = popover.querySelector("input");
    const plusButton = popover.querySelector("#paginate-page-plus");
    const minusButton = popover.querySelector("#paginate-page-minus");
    const goButton = popover.querySelector("#paginate-page-go");

    // Plus button handler
    plusButton.addEventListener("click", () => {
        let val = parseInt(pageInput.value) || 1;
        pageInput.value = Math.min(pageMax, val + 1);
    });

    // Minus button handler
    minusButton.addEventListener("click", () => {
        let val = parseInt(pageInput.value) || 1;
        pageInput.value = Math.max(1, val - 1);
    });

    // Go button handler
    goButton.addEventListener("click", () => {
        const page = parseInt(pageInput.value) || 1;
        
        // Parse current URL query params
        const url = new URL(window.location.href);
        const originalParams = new URLSearchParams(url.search);

        // Build new params
        const newParams = new URLSearchParams();

        if (page !== 1) {
            newParams.set("page", page);
        }

        // Append all other params except 'page'
        for (const [key, value] of originalParams.entries()) {
            if (key !== "page") {
                newParams.append(key, value);
            }
        }

        // Rebuild and navigate
        window.location.href = `${url.pathname}?${newParams.toString()}`;
    });

    // Close popover if clicking outside
    function handleClickOutside(event) {
        if (!popover.contains(event.target) && !element.contains(event.target)) {
            // Use jQuery just to hide the popover
            $(element).popover("hide");
            document.removeEventListener("mousedown", handleClickOutside);
        }
    }

    // Defer to next tick so it doesn't close immediately
    setTimeout(() => {
        document.addEventListener("mousedown", handleClickOutside);
    }, 0);

    // Cleanup on hide
    $(element).on("hidden.bs.popover", function () {
        $(element).popover("dispose");
    });
}

var paginateGoTos = document.querySelectorAll(".paginate-goto");
if (paginateGoTos) {
    paginateGoTos.forEach(function(paginateGoTo) {
        paginateGoTo.addEventListener("click", function(event) {
            event.preventDefault();
            openGoToPagePopover(event.currentTarget);
        });
    });
}