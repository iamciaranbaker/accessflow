/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./frontend/index.js":
/*!***************************!*\
  !*** ./frontend/index.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _src_css_main_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./src/css/main.css */ \"./frontend/src/css/main.css\");\n/* harmony import */ var _src_js_sidebar_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./src/js/sidebar.js */ \"./frontend/src/js/sidebar.js\");\n/* harmony import */ var _src_js_password_reveal_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./src/js/password_reveal.js */ \"./frontend/src/js/password_reveal.js\");\n/* harmony import */ var _src_js_password_reveal_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_src_js_password_reveal_js__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var _src_js_confirmation_modal_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./src/js/confirmation_modal.js */ \"./frontend/src/js/confirmation_modal.js\");\n/* harmony import */ var _src_js_delete_user_modal_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./src/js/delete_user_modal.js */ \"./frontend/src/js/delete_user_modal.js\");\n/* harmony import */ var _src_js_delete_service_modal_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./src/js/delete_service_modal.js */ \"./frontend/src/js/delete_service_modal.js\");\n/* harmony import */ var _src_js_autofocus_js__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./src/js/autofocus.js */ \"./frontend/src/js/autofocus.js\");\n/* harmony import */ var _src_js_autofocus_js__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_src_js_autofocus_js__WEBPACK_IMPORTED_MODULE_6__);\n/* harmony import */ var _src_js_flash_messages_js__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./src/js/flash_messages.js */ \"./frontend/src/js/flash_messages.js\");\n/* harmony import */ var _src_js_flash_messages_js__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_src_js_flash_messages_js__WEBPACK_IMPORTED_MODULE_7__);\n/* harmony import */ var _src_js_card_heights_js__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./src/js/card_heights.js */ \"./frontend/src/js/card_heights.js\");\n/* harmony import */ var _src_js_card_heights_js__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_src_js_card_heights_js__WEBPACK_IMPORTED_MODULE_8__);\n/* harmony import */ var _src_js_pagination_popover_js__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./src/js/pagination_popover.js */ \"./frontend/src/js/pagination_popover.js\");\n/* harmony import */ var _src_js_pagination_popover_js__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_src_js_pagination_popover_js__WEBPACK_IMPORTED_MODULE_9__);\n/* harmony import */ var _src_js_filter_popover_js__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./src/js/filter_popover.js */ \"./frontend/src/js/filter_popover.js\");\n/* harmony import */ var _src_js_filter_popover_js__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_src_js_filter_popover_js__WEBPACK_IMPORTED_MODULE_10__);\n/* harmony import */ var _src_js_create_request_js__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./src/js/create_request.js */ \"./frontend/src/js/create_request.js\");\n/* harmony import */ var _src_js_create_request_js__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_src_js_create_request_js__WEBPACK_IMPORTED_MODULE_11__);\n/* harmony import */ var _src_js_decline_request_modal_js__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./src/js/decline_request_modal.js */ \"./frontend/src/js/decline_request_modal.js\");\n// CSS\n\n\n// JavaScript\n\n\n\n\n\n\n\n\n\n\n\n\n\n//# sourceURL=webpack://AccessFlow/./frontend/index.js?");

/***/ }),

/***/ "./frontend/src/js/autofocus.js":
/*!**************************************!*\
  !*** ./frontend/src/js/autofocus.js ***!
  \**************************************/
/***/ (() => {

eval("// Find the first element with 'is-invalid'\nconst firstInvalid = document.querySelector(\".form-control.is-invalid\");\nif (firstInvalid) {\n  // Set autofocus on the first invalid input\n  firstInvalid.focus();\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/autofocus.js?");

/***/ }),

/***/ "./frontend/src/js/card_heights.js":
/*!*****************************************!*\
  !*** ./frontend/src/js/card_heights.js ***!
  \*****************************************/
/***/ (() => {

eval("const mainHeader = document.querySelector(\".main-header\");\nconst contentHeader = document.querySelector(\".content-header\");\nconst mainFooter = document.querySelector(\".main-footer\");\nconst logsContainer = document.querySelector(\".job-logs\");\nif (mainHeader && contentHeader && mainFooter) {\n  // Calculate the available vertical space\n  const availableHeight = window.innerHeight - mainHeader.offsetHeight - contentHeader.offsetHeight - mainFooter.offsetHeight - 16;\n  const logsContainer = document.querySelector(\".job-logs\");\n  const permissionsCard = document.querySelector(\".user-permissions\");\n  if (logsContainer) {\n    // Set the available height as the logs container's maximum height\n    logsContainer.style.maxHeight = availableHeight + \"px\";\n    logsContainer.scrollTop = logsContainer.scrollHeight;\n  }\n  if (permissionsCard) {\n    // Set the available height as the permissions card's maximum height\n    permissionsCard.style.maxHeight = availableHeight + \"px\";\n  }\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/card_heights.js?");

/***/ }),

/***/ "./frontend/src/js/confirmation_modal.js":
/*!***********************************************!*\
  !*** ./frontend/src/js/confirmation_modal.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   openConfirmationModal: () => (/* binding */ openConfirmationModal),\n/* harmony export */   openDeleteConfirmationModal: () => (/* binding */ openDeleteConfirmationModal)\n/* harmony export */ });\n// Open the confirmation modal dynamically\nfunction openConfirmationModal(modalTitle, modalText, buttonText, buttonUrl, hasConfirmation = false, confirmationValue = \"\") {\n  // Conditionally render the confirmation section\n  let modalBodyHtml = \"\";\n  if (hasConfirmation) {\n    modalBodyHtml = `\n            <p>${modalText}</p>\n            <p>Type the following to confirm:</p>\n            <code>${confirmationValue}</code>\n            <input type=\"text\" class=\"form-control mt-4\" required>\n        `;\n  } else {\n    modalBodyHtml = `\n            <p class=\"mb-0\">${modalText}</p>\n        `;\n  }\n  const modalHtml = `\n        <div class=\"modal fade\" id=\"confirmation-modal\">\n            <div class=\"modal-dialog modal-lg\">\n                <div class=\"modal-content\">\n                    <div class=\"modal-header\">\n                        <h4 class=\"modal-title\">${modalTitle}</h4>\n                        <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\">\n                            <span aria-hidden=\"true\">&times;</span>\n                        </button>\n                    </div>\n                    <div class=\"modal-body\">\n                        ${modalBodyHtml}\n                    </div>\n                    <div class=\"modal-footer justify-content-between\">\n                        <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">Cancel</button>\n                        <button type=\"button\" class=\"btn btn-danger\">${buttonText}</button>\n                    </div>\n                </div>\n            </div>\n        </div>\n    `;\n\n  // Append modal HTML to the body\n  document.body.insertAdjacentHTML(\"beforeend\", modalHtml);\n\n  // Fetch the action button element\n  var button = document.querySelector(\"#confirmation-modal .modal-footer .btn-danger\");\n  if (hasConfirmation) {\n    // Fetch the input element\n    var input = document.querySelector(\"#confirmation-modal .modal-body input\");\n    // Disable the button by default\n    button.disabled = true;\n\n    // Add an event listener to the input field to check text and enable button\n    input.addEventListener(\"input\", function () {\n      if (input.value === confirmationValue) {\n        button.disabled = false;\n      } else {\n        button.disabled = true;\n      }\n    });\n  }\n\n  // Show the modal - uses jQuery\n  $(\"#confirmation-modal\").modal(\"show\");\n\n  // Handle the button click\n  button.addEventListener(\"click\", function () {\n    if (!button.disabled) {\n      window.location.href = buttonUrl;\n    }\n  });\n\n  // Remove modal from DOM after it is closed - uses jQuery\n  $(\"#confirmation-modal\").on(\"hidden.bs.modal\", function () {\n    $(this).remove();\n  });\n}\nfunction openDeleteConfirmationModal(itemType, deleteUrl, confirmationValue) {\n  openConfirmationModal(`Delete ${itemType}`, `Are you sure you want to delete this ${itemType.toLowerCase()}?`, `Delete ${itemType}`, deleteUrl, true, confirmationValue);\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/confirmation_modal.js?");

/***/ }),

/***/ "./frontend/src/js/create_request.js":
/*!*******************************************!*\
  !*** ./frontend/src/js/create_request.js ***!
  \*******************************************/
/***/ (() => {

eval("// Only run if we are on the frontend create request page\nif (window.location.pathname.toLowerCase().startsWith(\"/requests/create\")) {\n  const queryParams = new URLSearchParams(window.location.search);\n  const requestType = queryParams.get(\"type\");\n  if (queryParams && requestType && (requestType == \"account_creation\" || requestType == \"service_access\")) {\n    const environmentSelect = document.querySelector('select[name=\"environments\"]');\n    const nonProdPIDInput = document.querySelector('input[name=\"nonprod_pid\"]');\n    const nonProdSSHKeyInput = document.querySelector('textarea[name=\"nonprod_ssh_key\"]');\n    const prodPIDInput = document.querySelector('input[name=\"prod_pid\"]');\n    const prodSSHKeyInput = document.querySelector('textarea[name=\"prod_ssh_key\"]');\n    const scClearanceInputs = document.querySelectorAll('input[name=\"sc_clearance\"]');\n    const nonProdPIDGroup = nonProdPIDInput.closest(\".form-group\");\n    const prodPIDGroup = prodPIDInput.closest(\".form-group\");\n    const scClearanceGroup = scClearanceInputs[0]?.closest(\".form-group\");\n    if (requestType == \"account_creation\" && nonProdSSHKeyInput) var nonProdSSHKeyGroup = nonProdSSHKeyInput.closest(\".form-group\");\n    if (requestType == \"account_creation\" && prodSSHKeyInput) var prodSSHKeyGroup = prodSSHKeyInput.closest(\".form-group\");\n\n    // Store original min/max values so we can restore them later\n    const nonProdMin = nonProdPIDInput.getAttribute(\"minlength\");\n    const nonProdMax = nonProdPIDInput.getAttribute(\"maxlength\");\n    const prodMin = prodPIDInput.getAttribute(\"minlength\");\n    const prodMax = prodPIDInput.getAttribute(\"maxlength\");\n\n    // Activate Select2\n    $(\".select2\").select2();\n    function updateEnvironmentVisibility() {\n      const selectedValues = Array.from(environmentSelect.selectedOptions).map(opt => opt.value);\n\n      // Toggle Non-Prod PID\n      if (selectedValues.includes(\"nonprod\")) {\n        nonProdPIDGroup.style.display = \"block\";\n        nonProdPIDInput.setAttribute(\"required\", \"\");\n        nonProdPIDInput.setAttribute(\"minlength\", nonProdMin);\n        nonProdPIDInput.setAttribute(\"maxlength\", nonProdMax);\n        if (requestType == \"account_creation\") {\n          nonProdSSHKeyGroup.style.display = \"block\";\n          nonProdPIDInput.setAttribute(\"required\", \"\");\n        }\n      } else {\n        nonProdPIDGroup.style.display = \"none\";\n        nonProdPIDInput.removeAttribute(\"required\");\n        nonProdPIDInput.removeAttribute(\"minlength\");\n        nonProdPIDInput.removeAttribute(\"maxlength\");\n        if (requestType == \"account_creation\") {\n          nonProdSSHKeyGroup.style.display = \"none\";\n          nonProdPIDInput.removeAttribute(\"required\");\n        }\n      }\n\n      // Toggle Prod PID and SC Clearance\n      if (selectedValues.includes(\"prod\")) {\n        prodPIDGroup.style.display = \"block\";\n        prodPIDInput.setAttribute(\"required\", \"\");\n        prodPIDInput.setAttribute(\"minlength\", prodMin);\n        prodPIDInput.setAttribute(\"maxlength\", prodMax);\n        if (requestType == \"account_creation\") {\n          prodSSHKeyGroup.style.display = \"block\";\n          prodPIDInput.setAttribute(\"required\", \"\");\n        }\n        scClearanceGroup.style.display = \"block\";\n        scClearanceInputs.forEach(input => input.setAttribute(\"required\", \"\"));\n      } else {\n        prodPIDGroup.style.display = \"none\";\n        prodPIDInput.removeAttribute(\"required\");\n        prodPIDInput.removeAttribute(\"minlength\");\n        prodPIDInput.removeAttribute(\"maxlength\");\n        if (requestType == \"account_creation\") {\n          prodSSHKeyGroup.style.display = \"none\";\n          prodPIDInput.removeAttribute(\"required\");\n        }\n        scClearanceGroup.style.display = \"none\";\n        scClearanceInputs.forEach(input => input.removeAttribute(\"required\"));\n      }\n    }\n\n    // Initial state on page load\n    updateEnvironmentVisibility();\n\n    // Attach change event to select element\n    $(environmentSelect).on(\"change\", updateEnvironmentVisibility);\n  }\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/create_request.js?");

/***/ }),

/***/ "./frontend/src/js/decline_request_modal.js":
/*!**************************************************!*\
  !*** ./frontend/src/js/decline_request_modal.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _confirmation_modal_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./confirmation_modal.js */ \"./frontend/src/js/confirmation_modal.js\");\n\n\n// Attach the decline button with event listener\nconst requestDeclineButton = document.querySelector(\".request-decline\");\nif (requestDeclineButton) {\n  requestDeclineButton.addEventListener(\"click\", function (event) {\n    event.preventDefault();\n\n    // Open the confirmation modal\n    (0,_confirmation_modal_js__WEBPACK_IMPORTED_MODULE_0__.openConfirmationModal)(\"Decline Request #1\", \"Are you sure you want to decline this request?\", \"Decline Request\", \"\", false);\n  });\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/decline_request_modal.js?");

/***/ }),

/***/ "./frontend/src/js/delete_service_modal.js":
/*!*************************************************!*\
  !*** ./frontend/src/js/delete_service_modal.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _confirmation_modal_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./confirmation_modal.js */ \"./frontend/src/js/confirmation_modal.js\");\n\n\n// Attach the delete button with event listener in the service list\nvar serviceDeleteButtons = document.querySelectorAll(\".service-delete\");\nif (serviceDeleteButtons) {\n  serviceDeleteButtons.forEach(function (deleteButton) {\n    deleteButton.addEventListener(\"click\", function (event) {\n      var serviceRow = event.target.closest(\"tr\");\n      var serviceId = serviceRow.getAttribute(\"data-service-id\");\n      var serviceName = serviceRow.getAttribute(\"data-service-name\");\n\n      // Open the confirmation modal for service deletion\n      (0,_confirmation_modal_js__WEBPACK_IMPORTED_MODULE_0__.openDeleteConfirmationModal)(\"Service\", `/admin/services/delete?id=${serviceId}`, serviceName);\n    });\n  });\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/delete_service_modal.js?");

/***/ }),

/***/ "./frontend/src/js/delete_user_modal.js":
/*!**********************************************!*\
  !*** ./frontend/src/js/delete_user_modal.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _confirmation_modal_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./confirmation_modal.js */ \"./frontend/src/js/confirmation_modal.js\");\n\n\n// Attach the delete button with event listener in the user list\nvar userDeleteButtons = document.querySelectorAll(\".user-delete\");\nif (userDeleteButtons) {\n  userDeleteButtons.forEach(function (deleteButton) {\n    deleteButton.addEventListener(\"click\", function (event) {\n      var userRow = event.target.closest(\"tr\");\n      var userId = userRow.getAttribute(\"data-user-id\");\n      var userEmailAddress = userRow.getAttribute(\"data-user-email-address\");\n\n      // Open the confirmation modal for user deletion\n      (0,_confirmation_modal_js__WEBPACK_IMPORTED_MODULE_0__.openDeleteConfirmationModal)(\"User\", `/admin/users/delete?id=${userId}`, userEmailAddress);\n    });\n  });\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/delete_user_modal.js?");

/***/ }),

/***/ "./frontend/src/js/filter_popover.js":
/*!*******************************************!*\
  !*** ./frontend/src/js/filter_popover.js ***!
  \*******************************************/
/***/ (() => {

eval("function openFilterPopover(element, filters = []) {\n  // Remove existing popover\n  $(element).popover(\"dispose\");\n\n  // Build popover content\n  let filterFieldsHtml = \"\";\n  filters.forEach(filter => {\n    filterFieldsHtml += `\n            <div class=\"form-group mb-1\">\n                <label class=\"col-form-label\" for=\"${filter.name}\">${filter.label}</label>\n                <select name=\"${filter.name}\" class=\"form-control form-control-sm select2\" multiple>\n                    ${filter.options.map(option => `\n                        <option value=\"${option.value}\">${option.label}</option>\n                    `).join('')}\n                </select>\n            </div>\n        `;\n  });\n  const popoverHtml = `\n        <div>\n            <form style=\"min-width: 250px\">\n                ${filterFieldsHtml}\n                <button type=\"submit\" class=\"btn btn-primary btn-sm btn-block mt-3\">Apply Filter(s)</button>\n            </form>\n        </div>\n    `;\n\n  // Initialize popover\n  $(element).popover({\n    html: true,\n    content: popoverHtml,\n    title: \"Apply Filter(s)\",\n    placement: \"bottom\",\n    container: \"body\",\n    trigger: \"manual\",\n    animation: true,\n    sanitize: false\n  });\n\n  // Show popover\n  $(element).popover(\"show\");\n\n  // After popover is shown, initialize Select2 and event listeners\n  const popoverId = element.getAttribute(\"aria-describedby\");\n  const popover = document.getElementById(popoverId);\n  if (!popover) return;\n  const $popover = $(\"#\" + popoverId);\n  const $form = $popover.find(\"form\");\n  const urlParams = new URLSearchParams(window.location.search);\n\n  // Pre-select values based on URL params\n  filters.forEach(filter => {\n    const selectedValues = urlParams.getAll(`filter[${filter.name}]`);\n    const $select = $popover.find(`select[name=\"${filter.name}\"]`);\n    $select.find(\"option\").each(function () {\n      if (selectedValues.includes(this.value)) {\n        $(this).prop(\"selected\", true);\n      }\n    });\n\n    // Initialize Select2 on live DOM element, point dropdownParent to popover\n    $select.select2({\n      dropdownParent: $popover,\n      closeOnSelect: true,\n      theme: \"bootstrap4\"\n    });\n  });\n\n  // Add form submit listener\n  $form.on(\"submit\", function (event) {\n    event.preventDefault();\n    const data = new FormData(this);\n    const newParams = new URLSearchParams();\n\n    // Preserve existing non-filter params, excluding \"page\"\n    const currentParams = new URLSearchParams(window.location.search);\n    for (const [key, value] of currentParams.entries()) {\n      if (!key.startsWith(\"filter[\") && key !== \"page\") {\n        newParams.append(key, value);\n      }\n    }\n\n    // Add filters\n    for (const [key, value] of data.entries()) {\n      if (value.trim()) {\n        newParams.append(`filter[${key}]`, value.trim());\n      }\n    }\n\n    // Build redirect URL\n    const queryString = newParams.toString();\n    if (queryString) {\n      window.location.href = `${window.location.pathname}?${queryString}`;\n    } else {\n      window.location.href = window.location.pathname;\n    }\n  });\n\n  // Close popover if clicking outside\n  function handleClickOutside(event) {\n    if (!popover.contains(event.target) && !element.contains(event.target)) {\n      $(element).popover(\"hide\");\n      document.removeEventListener(\"mousedown\", handleClickOutside);\n    }\n  }\n  setTimeout(() => {\n    document.addEventListener(\"mousedown\", handleClickOutside);\n  }, 0);\n  $(element).on(\"hidden.bs.popover\", function () {\n    $(element).popover(\"dispose\");\n  });\n}\nconst filterButton = document.querySelector(\".filter\");\nif (filterButton) {\n  filterButton.addEventListener(\"click\", function (event) {\n    event.preventDefault();\n    openFilterPopover(this, filterOptions);\n  });\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/filter_popover.js?");

/***/ }),

/***/ "./frontend/src/js/flash_messages.js":
/*!*******************************************!*\
  !*** ./frontend/src/js/flash_messages.js ***!
  \*******************************************/
/***/ (() => {

eval("// Map categories to Toastr types\nconst categoryMap = {\n  success: \"success\",\n  danger: \"error\",\n  warning: \"warning\",\n  info: \"info\"\n};\n\n// Toastr options\ntoastr.options = {\n  closeButton: true,\n  progressBar: true,\n  positionClass: \"toast-top-right\",\n  timeOut: \"10000\" // 10 seconds in milliseconds\n};\n\n// Get flash messages\nconst flashMessagesContainer = document.getElementById(\"flash-messages\");\n// Check the flash messages container exists as it might not if there are no messages\nif (flashMessagesContainer) {\n  const flashMessages = flashMessagesContainer.querySelectorAll(\".flash-message\");\n\n  // Display each flash message as a Toastr notification\n  flashMessages.forEach(flashMessage => {\n    const category = flashMessage.dataset.category; // Get message category\n    const message = flashMessage.textContent.trim(); // Get message text\n    const toastrType = categoryMap[category] || \"info\"; // Map category to Toastr type, default to 'info' if not found\n    toastr[toastrType](message);\n  });\n  flashMessagesContainer.remove();\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/flash_messages.js?");

/***/ }),

/***/ "./frontend/src/js/pagination_popover.js":
/*!***********************************************!*\
  !*** ./frontend/src/js/pagination_popover.js ***!
  \***********************************************/
/***/ (() => {

eval("function openGoToPagePopover(element) {\n  // Remove any existing popover\n  $(element).popover(\"dispose\");\n  const page = element.getAttribute(\"data-page\");\n  const pageMax = element.getAttribute(\"data-page-max\");\n  const popoverHtml = `\n        <div class=\"input-group\">\n            <input type=\"number\" class=\"form-control\" id=\"pageNumberInput\" min=\"1\" max=\"${pageMax}\" value=\"${page}\" step=\"1\">\n            <div class=\"input-group-append\">\n                <button class=\"btn btn-default\" type=\"button\" id=\"paginate-page-plus\">\n                    <i class=\"fas fa-plus\"></i>\n                </button>\n                <button class=\"btn btn-default\" type=\"button\" id=\"paginate-page-minus\">\n                    <i class=\"fas fa-minus\"></i>\n                </button>\n            </div>\n        </div>\n        <button class=\"btn btn-primary btn-sm btn-block mt-2\" id=\"paginate-page-go\">Go To Page</button>\n    `;\n\n  // Initialize popover\n  $(element).popover({\n    html: true,\n    content: popoverHtml,\n    title: \"Go To Page\",\n    placement: \"top\",\n    container: \"body\",\n    trigger: \"manual\",\n    animation: true,\n    sanitize: false\n  });\n  // Show the popover\n  $(element).popover(\"show\");\n\n  // After popover is shown, attach logic\n  const popoverId = element.getAttribute(\"aria-describedby\");\n  const popover = document.getElementById(popoverId);\n  if (!popover) return;\n  const pageInput = popover.querySelector(\"input\");\n  const plusButton = popover.querySelector(\"#paginate-page-plus\");\n  const minusButton = popover.querySelector(\"#paginate-page-minus\");\n  const goButton = popover.querySelector(\"#paginate-page-go\");\n\n  // Plus button handler\n  plusButton.addEventListener(\"click\", () => {\n    let val = parseInt(pageInput.value) || 1;\n    pageInput.value = Math.min(pageMax, val + 1);\n  });\n\n  // Minus button handler\n  minusButton.addEventListener(\"click\", () => {\n    let val = parseInt(pageInput.value) || 1;\n    pageInput.value = Math.max(1, val - 1);\n  });\n\n  // Go button handler\n  goButton.addEventListener(\"click\", () => {\n    const page = parseInt(pageInput.value) || 1;\n\n    // Parse current URL query params\n    const url = new URL(window.location.href);\n    const originalParams = new URLSearchParams(url.search);\n\n    // Build new params\n    const newParams = new URLSearchParams();\n    if (page !== 1) {\n      newParams.set(\"page\", page);\n    }\n\n    // Append all other params except 'page'\n    for (const [key, value] of originalParams.entries()) {\n      if (key !== \"page\") {\n        newParams.append(key, value);\n      }\n    }\n\n    // Rebuild and navigate\n    window.location.href = `${url.pathname}?${newParams.toString()}`;\n  });\n\n  // Close popover if clicking outside\n  function handleClickOutside(event) {\n    if (!popover.contains(event.target) && !element.contains(event.target)) {\n      // Use jQuery just to hide the popover\n      $(element).popover(\"hide\");\n      document.removeEventListener(\"mousedown\", handleClickOutside);\n    }\n  }\n\n  // Defer to next tick so it doesn't close immediately\n  setTimeout(() => {\n    document.addEventListener(\"mousedown\", handleClickOutside);\n  }, 0);\n\n  // Cleanup on hide\n  $(element).on(\"hidden.bs.popover\", function () {\n    $(element).popover(\"dispose\");\n  });\n}\nvar paginateGoTos = document.querySelectorAll(\".paginate-goto\");\nif (paginateGoTos) {\n  paginateGoTos.forEach(function (paginateGoTo) {\n    paginateGoTo.addEventListener(\"click\", function (event) {\n      event.preventDefault();\n      openGoToPagePopover(event.currentTarget);\n    });\n  });\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/pagination_popover.js?");

/***/ }),

/***/ "./frontend/src/js/password_reveal.js":
/*!********************************************!*\
  !*** ./frontend/src/js/password_reveal.js ***!
  \********************************************/
/***/ (() => {

eval("// Attach event listener to all toggle-password buttons on the page\nvar togglePasswordButtons = document.querySelectorAll(\".toggle-password\");\nif (togglePasswordButtons) {\n  togglePasswordButtons.forEach(function (togglePasswordButton) {\n    // Add a tooltip to the button\n    togglePasswordButton.setAttribute(\"title\", \"Reveal \" + togglePasswordButton.getAttribute(\"data-tooltip\"));\n    togglePasswordButton.addEventListener(\"click\", function () {\n      // Find the input associated with this button\n      var inputGroup = togglePasswordButton.closest(\".input-group\");\n      var input = inputGroup.querySelector(\"input\");\n      var icon = togglePasswordButton.querySelector(\"i\");\n\n      // Toggle the visibility of the password\n      if (input.type === \"password\") {\n        input.type = \"text\";\n        icon.classList.remove(\"fa-eye\");\n        icon.classList.add(\"fa-eye-slash\");\n        togglePasswordButton.setAttribute(\"title\", \"Conceal \" + togglePasswordButton.getAttribute(\"data-tooltip\"));\n      } else {\n        input.type = \"password\";\n        icon.classList.remove(\"fa-eye-slash\");\n        icon.classList.add(\"fa-eye\");\n        togglePasswordButton.setAttribute(\"title\", \"Reveal \" + togglePasswordButton.getAttribute(\"data-tooltip\"));\n      }\n    });\n  });\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/password_reveal.js?");

/***/ }),

/***/ "./frontend/src/js/sidebar.js":
/*!************************************!*\
  !*** ./frontend/src/js/sidebar.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _utils_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./utils.js */ \"./frontend/src/js/utils.js\");\n\nvar collapseButton = document.querySelector(\"[data-widget='pushmenu']\");\nfunction updateTooltips() {\n  // Check if the sidebar is in a collapsed state\n  var isCollapsed = document.querySelector(\"body\").classList.contains(\"sidebar-collapse\");\n\n  // Iterate through all items in sidebar\n  document.querySelectorAll(\".nav-sidebar .nav-link\").forEach(link => {\n    if (isCollapsed) {\n      // Set the title if sidebar is collapsed\n      link.setAttribute(\"title\", link.getAttribute(\"data-tooltip\"));\n    } else {\n      // Remove the title if sidebar is not collapsed\n      link.removeAttribute(\"title\");\n    }\n  });\n\n  // Save the sidebar state to a browser cookie\n  (0,_utils_js__WEBPACK_IMPORTED_MODULE_0__.setCookie)(\"sidebarCollapsed\", isCollapsed);\n}\n\n// Make sure the collapse button actually exists...\nif (collapseButton) {\n  // Listen for clicks on the sidebar collapse button\n  collapseButton.addEventListener(\"click\", function () {\n    // Use a timeout to wait for the collapsed state to toggle\n    setTimeout(updateTooltips, 100);\n  });\n}\n\n// Apply the sidebar state from the cookie\nvar sidebarCollapsed = (0,_utils_js__WEBPACK_IMPORTED_MODULE_0__.getCookie)(\"sidebarCollapsed\");\nif (sidebarCollapsed === \"true\" && !document.body.classList.contains(\"sidebar-collapse\")) {\n  // Simulate a click of the sidebar collapse button\n  collapseButton.click();\n}\n\n// Initial check to set correct tooltip state on page load\nupdateTooltips();\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/sidebar.js?");

/***/ }),

/***/ "./frontend/src/js/utils.js":
/*!**********************************!*\
  !*** ./frontend/src/js/utils.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   getCookie: () => (/* binding */ getCookie),\n/* harmony export */   setCookie: () => (/* binding */ setCookie)\n/* harmony export */ });\nfunction getCookie(name) {\n  const value = `; ${document.cookie}`;\n  const parts = value.split(`; ${name}=`);\n  if (parts.length === 2) {\n    return parts.pop().split(\";\").shift();\n  }\n}\nfunction setCookie(name, value) {\n  document.cookie = `${name}=${value}; path=/`;\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/utils.js?");

/***/ }),

/***/ "./frontend/src/css/main.css":
/*!***********************************!*\
  !*** ./frontend/src/css/main.css ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n// extracted by mini-css-extract-plugin\n\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/css/main.css?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./frontend/index.js");
/******/ 	
/******/ })()
;