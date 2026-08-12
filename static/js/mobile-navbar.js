document.addEventListener("DOMContentLoaded", function () {
    const hamburger = document.getElementById("mobileHamburger");
    const sidebar = document.getElementById("mobileSidebar");
    const overlay = document.getElementById("sidebarOverlay");
    const closeBtn = document.getElementById("closeSidebar");

    function openSidebar() {
        sidebar.classList.add("active");
        overlay.classList.add("active");
        document.body.style.overflow = "hidden";
        document.body.style.touchAction = "none"; // Hard lock for mobile
    }

    function closeSidebarFunc() {
        sidebar.classList.remove("active");
        overlay.classList.remove("active");
        document.body.style.overflow = ""; 
        document.body.style.touchAction = "";
    }

    // Escape key to close
    document.addEventListener("keydown", function(e) {
        if (e.key === "Escape" && sidebar.classList.contains("active")) {
            closeSidebarFunc();
        }
    });

    if (hamburger) hamburger.addEventListener("click", openSidebar);
    if (closeBtn) closeBtn.addEventListener("click", closeSidebarFunc);
    if (overlay) overlay.addEventListener("click", closeSidebarFunc);

    // Accordion Logic
    const accordionToggles = document.querySelectorAll(".mobile-accordion-toggle");
    
    accordionToggles.forEach(toggle => {
        toggle.addEventListener("click", function(e) {
            e.preventDefault();
            const targetId = this.getAttribute("data-target");
            const content = document.getElementById(targetId);
            
            // Toggle current
            this.classList.toggle("open");
            if (this.classList.contains("open")) {
                content.classList.add("open");
                // dynamically adjust max-height if content is very long, but 500px usually suffices.
                content.style.maxHeight = content.scrollHeight + "px";
            } else {
                content.classList.remove("open");
                content.style.maxHeight = "0";
            }
        });
    });
});
