document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.getElementById("servicesToggle");
    const menu = document.getElementById("servicesDropdown");

    if (!toggle || !menu) return;

    toggle.addEventListener("click", function (e) {

        if (window.innerWidth > 991) return;

        e.preventDefault();
        e.stopPropagation();

        menu.classList.toggle("show");

    });

    document.addEventListener("click", function (e) {

        if (
            !toggle.contains(e.target) &&
            !menu.contains(e.target)
        ) {
            menu.classList.remove("show");
        }

    });

});