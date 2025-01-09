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
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _src_css_main_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./src/css/main.css */ \"./frontend/src/css/main.css\");\n/* harmony import */ var _src_js_sidebar_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./src/js/sidebar.js */ \"./frontend/src/js/sidebar.js\");\n/* harmony import */ var _src_js_search_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./src/js/search.js */ \"./frontend/src/js/search.js\");\n/* harmony import */ var _src_js_search_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_src_js_search_js__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var _src_js_password_reveal_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./src/js/password_reveal.js */ \"./frontend/src/js/password_reveal.js\");\n/* harmony import */ var _src_js_password_reveal_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_src_js_password_reveal_js__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var _src_js_create_user_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./src/js/create_user.js */ \"./frontend/src/js/create_user.js\");\n/* harmony import */ var _src_js_create_user_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_src_js_create_user_js__WEBPACK_IMPORTED_MODULE_4__);\n\n\n\n\n\n\n//# sourceURL=webpack://access-flow/./frontend/index.js?");

/***/ }),

/***/ "./frontend/src/js/create_user.js":
/*!****************************************!*\
  !*** ./frontend/src/js/create_user.js ***!
  \****************************************/
/***/ (() => {

eval("document.addEventListener(\"DOMContentLoaded\", function () {\n  // Get the elements\n  var identityCard = document.querySelector('.user-identity');\n  var passwordCard = document.querySelector('.user-password');\n  var permissionsCard = document.querySelector('.user-permissions');\n\n  // Get the card heights\n  var identityHeight = identityCard.offsetHeight;\n  var passwordHeight = passwordCard.offsetHeight;\n\n  // Get vertical space between Identity and Password cards\n  var gap = passwordCard.getBoundingClientRect().top - identityCard.getBoundingClientRect().bottom;\n\n  // Calculate total height of left column (including gap)\n  var totalLeftHeight = identityHeight + passwordHeight + gap;\n\n  // Set the Permissions card body height\n  var permissionsHeader = permissionsCard.querySelector('.card-header').offsetHeight;\n  var permissionsFooter = permissionsCard.querySelector('.card-footer') ? permissionsCard.querySelector('.card-footer').offsetHeight : 0;\n  var permissionsBodyHeight = totalLeftHeight - permissionsHeader - permissionsFooter - 16;\n  var permissionsBody = permissionsCard.querySelector('.card-body');\n  var currentPermissionsBodyHeight = permissionsBody.offsetHeight;\n\n  // Only set the height if the current body height is larger than the calculated height\n  if (currentPermissionsBodyHeight > permissionsBodyHeight) {\n    permissionsBody.style.height = permissionsBodyHeight + 'px';\n  }\n});\n\n//# sourceURL=webpack://access-flow/./frontend/src/js/create_user.js?");

/***/ }),

/***/ "./frontend/src/js/password_reveal.js":
/*!********************************************!*\
  !*** ./frontend/src/js/password_reveal.js ***!
  \********************************************/
/***/ (() => {

eval("document.addEventListener(\"DOMContentLoaded\", function () {\n  // Attach event listener to all toggle-password buttons on the page.\n  var toggleButtons = document.querySelectorAll(\".toggle-password\");\n  toggleButtons.forEach(function (button) {\n    button.addEventListener(\"click\", function () {\n      // Find the input associated with this button.\n      var inputGroup = button.closest(\".input-group\");\n      var input = inputGroup.querySelector(\"input\");\n      var icon = button.querySelector(\"i\");\n\n      // Toggle the visibility of the password.\n      if (input.type === \"password\") {\n        input.type = \"text\";\n        icon.classList.remove(\"fa-eye\");\n        icon.classList.add(\"fa-eye-slash\");\n        button.setAttribute(\"title\", \"Conceal Password\");\n      } else {\n        input.type = \"password\";\n        icon.classList.remove(\"fa-eye-slash\");\n        icon.classList.add(\"fa-eye\");\n        button.setAttribute(\"title\", \"Reveal Password\");\n      }\n    });\n  });\n});\n\n//# sourceURL=webpack://access-flow/./frontend/src/js/password_reveal.js?");

/***/ }),

/***/ "./frontend/src/js/search.js":
/*!***********************************!*\
  !*** ./frontend/src/js/search.js ***!
  \***********************************/
/***/ (() => {

eval("document.addEventListener(\"DOMContentLoaded\", function () {\n  let debounceTimer;\n  const cache = {};\n  async function fetchSuggestions() {\n    const query = document.getElementById(\"searchInput\").value.trim().toLowerCase();\n    const suggestionsList = document.getElementById(\"searchSuggestionsList\");\n\n    // Hide suggestions if input is less than 2 characters.\n    if (query.length < 2) {\n      suggestionsList.style.display = \"none\";\n      return;\n    }\n\n    // Check if the result is already cached.\n    if (cache[query]) {\n      renderSearchSuggestions(cache[query]);\n      return;\n    }\n\n    // Debounce request to avoid sending too many requests.\n    clearTimeout(debounceTimer);\n    debounceTimer = setTimeout(async () => {\n      const response = await fetch(\"https://jsonplaceholder.typicode.com/users\");\n      const users = await response.json();\n      const suggestions = {\n        users: users.filter(user => user.name.toLowerCase().includes(query)).map(user => user.name),\n        groups: [\"Group A\", \"Group B\", \"Group C\"].filter(group => group.toLowerCase().includes(query)),\n        services: [\"Service 1\", \"Service 2\", \"Service 3\"].filter(service => service.toLowerCase().includes(query))\n      };\n\n      // Cache the result for future queries.\n      cache[query] = suggestions;\n      renderSuggestionsList(suggestions);\n    }, 100);\n  }\n  function renderSuggestionsList(suggestions) {\n    const suggestionsList = document.getElementById(\"searchSuggestionsList\");\n    suggestionsList.innerHTML = \"\";\n    suggestionsList.style.display = suggestions.users.length ? \"block\" : \"none\";\n    if (suggestions.users.length) {\n      const userHeading = document.createElement(\"li\");\n      userHeading.className = \"list-group-item list-group-item-info\";\n      userHeading.textContent = \"Users\";\n      suggestionsList.appendChild(userHeading);\n      suggestions.users.forEach(item => {\n        const listItem = document.createElement(\"li\");\n        listItem.className = \"list-group-item\";\n        listItem.textContent = item;\n        listItem.onclick = () => {\n          document.getElementById(\"searchInput\").value = item;\n          suggestionsList.style.display = \"none\";\n        };\n        suggestionsList.appendChild(listItem);\n      });\n    }\n  }\n\n  // Comment out until suggestions list design is finalised.\n  //document.querySelector(\"#searchInput\").addEventListener(\"input\", fetchSuggestions);\n});\n\n//# sourceURL=webpack://access-flow/./frontend/src/js/search.js?");

/***/ }),

/***/ "./frontend/src/js/sidebar.js":
/*!************************************!*\
  !*** ./frontend/src/js/sidebar.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _utils_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./utils.js */ \"./frontend/src/js/utils.js\");\n\ndocument.addEventListener(\"DOMContentLoaded\", function () {\n  var collapseButton = document.querySelector(\"[data-widget='pushmenu']\");\n  function updateTooltips() {\n    // Check if the sidebar is in a collapsed state.\n    var isCollapsed = document.querySelector(\"body\").classList.contains(\"sidebar-collapse\");\n\n    // Iterate through all items in sidebar.\n    document.querySelectorAll(\".nav-sidebar .nav-link\").forEach(link => {\n      if (isCollapsed) {\n        // Set the title if sidebar is collapsed.\n        link.setAttribute(\"title\", link.getAttribute(\"data-tooltip\"));\n      } else {\n        // Remove the title if sidebar is not collapsed.\n        link.removeAttribute(\"title\");\n      }\n    });\n\n    // Save the sidebar state to a browser cookie.\n    (0,_utils_js__WEBPACK_IMPORTED_MODULE_0__.setCookie)(\"sidebarCollapsed\", isCollapsed);\n  }\n\n  // Listen for clicks on the sidebar collapse button.\n  collapseButton.addEventListener(\"click\", function () {\n    // Use a timeout to wait for the collapsed state to toggle.\n    setTimeout(updateTooltips, 100);\n  });\n\n  // Apply the sidebar state from the cookie.\n  var sidebarCollapsed = (0,_utils_js__WEBPACK_IMPORTED_MODULE_0__.getCookie)(\"sidebarCollapsed\");\n  if (sidebarCollapsed === \"true\" && !document.body.classList.contains(\"sidebar-collapse\")) {\n    // Simulate a click of the sidebar collapse button.\n    collapseButton.click();\n  }\n\n  // Initial check to set correct tooltip state on page load.\n  updateTooltips();\n});\n\n//# sourceURL=webpack://access-flow/./frontend/src/js/sidebar.js?");

/***/ }),

/***/ "./frontend/src/js/utils.js":
/*!**********************************!*\
  !*** ./frontend/src/js/utils.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   getCookie: () => (/* binding */ getCookie),\n/* harmony export */   setCookie: () => (/* binding */ setCookie)\n/* harmony export */ });\nfunction getCookie(name) {\n  const value = `; ${document.cookie}`;\n  const parts = value.split(`; ${name}=`);\n  if (parts.length === 2) {\n    return parts.pop().split(\";\").shift();\n  }\n}\nfunction setCookie(name, value) {\n  document.cookie = `${name}=${value}; path=/`;\n}\n\n//# sourceURL=webpack://access-flow/./frontend/src/js/utils.js?");

/***/ }),

/***/ "./frontend/src/css/main.css":
/*!***********************************!*\
  !*** ./frontend/src/css/main.css ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n// extracted by mini-css-extract-plugin\n\n\n//# sourceURL=webpack://access-flow/./frontend/src/css/main.css?");

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