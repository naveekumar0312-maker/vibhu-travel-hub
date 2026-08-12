document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("toggleSidebar");
    const closeBtn = document.getElementById("closeSidebar");

    if (toggleBtn) {
        toggleBtn.addEventListener("click", function() {
            sidebar.classList.toggle("show");
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", function() {
            sidebar.classList.remove("show");
        });
    }

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});
