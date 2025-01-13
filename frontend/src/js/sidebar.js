import { getCookie, setCookie } from "./utils.js";

document.addEventListener("DOMContentLoaded", function() {
    var collapseButton = document.querySelector("[data-widget='pushmenu']");

    function updateTooltips() {
        // Check if the sidebar is in a collapsed state
        var isCollapsed = document.querySelector("body").classList.contains("sidebar-collapse");
        
        // Iterate through all items in sidebar
        document.querySelectorAll(".nav-sidebar .nav-link").forEach(link => {
            if (isCollapsed) {
                // Set the title if sidebar is collapsed
                link.setAttribute("title", link.getAttribute("data-tooltip"));
            } else {
                // Remove the title if sidebar is not collapsed
                link.removeAttribute("title");
            }
        });

        // Save the sidebar state to a browser cookie
        setCookie("sidebarCollapsed", isCollapsed);
    }

    // Listen for clicks on the sidebar collapse button
    collapseButton.addEventListener("click", function() {
        // Use a timeout to wait for the collapsed state to toggle
        setTimeout(updateTooltips, 100);
    });

    // Apply the sidebar state from the cookie
    var sidebarCollapsed = getCookie("sidebarCollapsed");
    if (sidebarCollapsed === "true" && !document.body.classList.contains("sidebar-collapse")) {
        // Simulate a click of the sidebar collapse button
        collapseButton.click();
    }

    // Initial check to set correct tooltip state on page load
    updateTooltips();
});