// static/js/main.js

document.addEventListener("DOMContentLoaded", function () {
    console.log("HealthGuard JS Loaded");

    // Example: Show a message on login/register page
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = "none";
        }, 4000);
    });

    // Example: Password toggle
    const togglePassword = document.querySelector("#togglePassword");
    const passwordInput = document.querySelector("#password");
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener("click", function () {
            const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
            passwordInput.setAttribute("type", type);
            this.classList.toggle("bi-eye");
        });
    }
});
