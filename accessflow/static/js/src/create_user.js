document.addEventListener("DOMContentLoaded", function() {
    // Get the elements
    var identityCard = document.querySelector('.user-identity');
    var passwordCard = document.querySelector('.user-password');
    var permissionsCard = document.querySelector('.user-permissions');

    // Get the card heights
    var identityHeight = identityCard.offsetHeight;
    var passwordHeight = passwordCard.offsetHeight;

    // Get vertical space between Identity and Password cards
    var gap = passwordCard.getBoundingClientRect().top - identityCard.getBoundingClientRect().bottom;

    // Calculate total height of left column (including gap)
    var totalLeftHeight = identityHeight + passwordHeight + gap;

    // Set the Permissions card body height
    var permissionsHeader = permissionsCard.querySelector('.card-header').offsetHeight;
    var permissionsFooter = permissionsCard.querySelector('.card-footer') ? permissionsCard.querySelector('.card-footer').offsetHeight : 0;
    var permissionsBodyHeight = totalLeftHeight - permissionsHeader - permissionsFooter - 16;

    var permissionsBody = permissionsCard.querySelector('.card-body');
    permissionsBody.style.height = permissionsBodyHeight + 'px';
});