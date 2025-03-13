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
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _src_css_main_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./src/css/main.css */ \"./frontend/src/css/main.css\");\n/* harmony import */ var _src_js_sidebar_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./src/js/sidebar.js */ \"./frontend/src/js/sidebar.js\");\n/* harmony import */ var _src_js_password_reveal_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./src/js/password_reveal.js */ \"./frontend/src/js/password_reveal.js\");\n/* harmony import */ var _src_js_password_reveal_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_src_js_password_reveal_js__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var _src_js_create_user_card_heights_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./src/js/create_user_card_heights.js */ \"./frontend/src/js/create_user_card_heights.js\");\n/* harmony import */ var _src_js_create_user_card_heights_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_src_js_create_user_card_heights_js__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var _src_js_delete_user_modal_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./src/js/delete_user_modal.js */ \"./frontend/src/js/delete_user_modal.js\");\n/* harmony import */ var _src_js_delete_user_modal_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_src_js_delete_user_modal_js__WEBPACK_IMPORTED_MODULE_4__);\n/* harmony import */ var _src_js_autofocus_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./src/js/autofocus.js */ \"./frontend/src/js/autofocus.js\");\n/* harmony import */ var _src_js_autofocus_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_src_js_autofocus_js__WEBPACK_IMPORTED_MODULE_5__);\n/* harmony import */ var _src_js_flash_messages_js__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./src/js/flash_messages.js */ \"./frontend/src/js/flash_messages.js\");\n/* harmony import */ var _src_js_flash_messages_js__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_src_js_flash_messages_js__WEBPACK_IMPORTED_MODULE_6__);\n\n\n\n\n\n\n\n\n//# sourceURL=webpack://AccessFlow/./frontend/index.js?");

/***/ }),

/***/ "./frontend/src/js/autofocus.js":
/*!**************************************!*\
  !*** ./frontend/src/js/autofocus.js ***!
  \**************************************/
/***/ (() => {

eval("// Find the first element with 'is-invalid'\nconst firstInvalid = document.querySelector(\".form-control.is-invalid\");\nif (firstInvalid) {\n  // Set autofocus on the first invalid input\n  firstInvalid.focus();\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/autofocus.js?");

/***/ }),

/***/ "./frontend/src/js/create_user_card_heights.js":
/*!*****************************************************!*\
  !*** ./frontend/src/js/create_user_card_heights.js ***!
  \*****************************************************/
/***/ (() => {

eval("// Get the card elements\nvar identityCard = document.querySelector(\".user-identity\");\nvar passwordCard = document.querySelector(\".user-password\");\nvar permissionsCard = document.querySelector(\".user-permissions\");\n\n// Ensure the cards actually exist (are we on the Create User page?)\nif (identityCard && passwordCard && permissionsCard) {\n  // Get the card heights\n  var identityHeight = identityCard.offsetHeight;\n  var passwordHeight = passwordCard.offsetHeight;\n\n  // Get vertical space between Identity and Password cards\n  var gap = passwordCard.getBoundingClientRect().top - identityCard.getBoundingClientRect().bottom;\n\n  // Calculate total height of left column (including gap)\n  var totalLeftHeight = identityHeight + passwordHeight + gap;\n\n  // Set the Permissions card body height\n  var permissionsHeader = permissionsCard.querySelector(\".card-header\").offsetHeight;\n  var permissionsFooter = permissionsCard.querySelector(\".card-footer\") ? permissionsCard.querySelector(\".card-footer\").offsetHeight : 0;\n  var permissionsBodyHeight = totalLeftHeight - permissionsHeader - permissionsFooter - 16;\n  var permissionsBody = permissionsCard.querySelector(\".card-body\");\n  var currentPermissionsBodyHeight = permissionsBody.offsetHeight;\n\n  // Only set the height if the current body height is larger than the calculated height\n  if (currentPermissionsBodyHeight > permissionsBodyHeight) {\n    permissionsBody.style.height = permissionsBodyHeight + \"px\";\n  }\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/create_user_card_heights.js?");

/***/ }),

/***/ "./frontend/src/js/delete_user_modal.js":
/*!**********************************************!*\
  !*** ./frontend/src/js/delete_user_modal.js ***!
  \**********************************************/
/***/ (() => {

eval("// Open the modal and set up the delete button link\nfunction openDeleteModal(userId, userEmail) {\n  var emailAddressText = document.getElementById(\"confirm-email-address\");\n  var emailAddressInput = document.getElementById(\"confirm-email-address-input\");\n  var deleteButton = document.getElementById(\"delete-user-btn\");\n  emailAddressText.innerHTML = userEmail;\n\n  // Set the delete button\"s data attribute to store the redirect URL\n  deleteButton.setAttribute(\"data-url\", \"/admin/users/\" + userId + \"/delete\");\n\n  // Reset the email input and disable the delete button\n  emailAddressInput.value = \"\";\n  deleteButton.disabled = true;\n\n  // Add an event listener to the input field to check email and enable button\n  emailAddressInput.addEventListener(\"input\", function () {\n    if (emailAddressInput.value === userEmail) {\n      deleteButton.disabled = false;\n    } else {\n      deleteButton.disabled = true;\n    }\n  });\n\n  // Show the modal\n  $(\"#delete-user-modal\").modal(\"show\");\n}\n\n// Attach the delete button with event listener in the user list\nvar userDeleteBtn = document.querySelectorAll(\".user-delete\");\nif (userDeleteBtn) {\n  userDeleteBtn.forEach(function (deleteButton) {\n    deleteButton.addEventListener(\"click\", function (event) {\n      var userRow = event.target.closest(\"tr\");\n      var userId = userRow.getAttribute(\"data-user-id\");\n      var userEmail = userRow.querySelector(\".user-email-address\").textContent.trim();\n      openDeleteModal(userId, userEmail);\n    });\n  });\n}\n\n// Handle delete button click and redirect\nvar deleteUserBtn = document.getElementById(\"delete-user-btn\");\nif (deleteUserBtn) {\n  deleteUserBtn.addEventListener(\"click\", function () {\n    if (!this.disabled) {\n      // Redirect to the delete URL\n      window.location.href = this.getAttribute(\"data-url\");\n    }\n  });\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/delete_user_modal.js?");

/***/ }),

/***/ "./frontend/src/js/flash_messages.js":
/*!*******************************************!*\
  !*** ./frontend/src/js/flash_messages.js ***!
  \*******************************************/
/***/ (() => {

eval("// Map categories to Toastr types\nconst categoryMap = {\n  success: \"success\",\n  danger: \"error\",\n  warning: \"warning\",\n  info: \"info\"\n};\n\n// Toastr options\ntoastr.options = {\n  closeButton: true,\n  progressBar: true,\n  positionClass: \"toast-top-right\",\n  timeOut: \"10000\" // 10 seconds in milliseconds\n};\n\n// Get flash messages\nconst flashMessagesContainer = document.getElementById(\"flash-messages\");\n// Check the flash messages container exists as it might not if there are no messages\nif (flashMessagesContainer) {\n  const flashMessages = flashMessagesContainer.querySelectorAll(\".flash-message\");\n\n  // Display each flash message as a Toastr notification\n  flashMessages.forEach(flashMessage => {\n    const category = flashMessage.dataset.category; // Get message category\n    const message = flashMessage.textContent.trim(); // Get message text\n    const toastrType = categoryMap[category] || \"info\"; // Map category to Toastr type, default to 'info' if not found\n    toastr[toastrType](message);\n  });\n}\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/flash_messages.js?");

/***/ }),

/***/ "./frontend/src/js/password_reveal.js":
/*!********************************************!*\
  !*** ./frontend/src/js/password_reveal.js ***!
  \********************************************/
/***/ (() => {

eval("// Attach event listener to all toggle-password buttons on the page\nvar toggleButtons = document.querySelectorAll(\".toggle-password\");\ntoggleButtons.forEach(function (button) {\n  // Add a tooltip to the button\n  button.setAttribute(\"title\", \"Reveal \" + button.getAttribute(\"data-tooltip\"));\n  button.addEventListener(\"click\", function () {\n    // Find the input associated with this button\n    var inputGroup = button.closest(\".input-group\");\n    var input = inputGroup.querySelector(\"input\");\n    var icon = button.querySelector(\"i\");\n\n    // Toggle the visibility of the password\n    if (input.type === \"password\") {\n      input.type = \"text\";\n      icon.classList.remove(\"fa-eye\");\n      icon.classList.add(\"fa-eye-slash\");\n      button.setAttribute(\"title\", \"Conceal \" + button.getAttribute(\"data-tooltip\"));\n    } else {\n      input.type = \"password\";\n      icon.classList.remove(\"fa-eye-slash\");\n      icon.classList.add(\"fa-eye\");\n      button.setAttribute(\"title\", \"Reveal \" + button.getAttribute(\"data-tooltip\"));\n    }\n  });\n});\n\n//# sourceURL=webpack://AccessFlow/./frontend/src/js/password_reveal.js?");

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