// Find the first element with 'is-invalid'
const firstInvalid = document.querySelector(".form-control.is-invalid");

if (firstInvalid) {
    // Set autofocus on the first invalid input
    firstInvalid.focus();
}