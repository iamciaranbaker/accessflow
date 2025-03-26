const mainHeader = document.querySelector(".main-header");
const contentHeader = document.querySelector(".content-header");
const mainFooter = document.querySelector(".main-footer");
const logsContainer = document.querySelector(".job-logs");

if (mainHeader && contentHeader && mainFooter) {
    // Calculate the available vertical space
    const availableHeight = window.innerHeight - mainHeader.offsetHeight - contentHeader.offsetHeight - mainFooter.offsetHeight - 16;

    const logsContainer = document.querySelector(".job-logs");
    const permissionsCard = document.querySelector(".user-permissions");

    if (logsContainer) {
        // Set the available height as the logs container's maximum height
        logsContainer.style.maxHeight = availableHeight + "px";
        logsContainer.scrollTop = logsContainer.scrollHeight;
    }
    if (permissionsCard) {
        // Set the available height as the permissions card's maximum height
        permissionsCard.style.maxHeight = availableHeight + "px";
    }
}