document.addEventListener("DOMContentLoaded", function () {
    const siteHeader = document.getElementById("siteHeader");
    
    if (siteHeader) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 80) {
                siteHeader.classList.add('scrolled');
            } else {
                siteHeader.classList.remove('scrolled');
            }
        });
    }
});
