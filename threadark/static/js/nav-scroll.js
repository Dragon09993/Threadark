document.addEventListener("DOMContentLoaded", function () {
    const nav = document.querySelector("nav");
    const offset = 100; // Adjust this to set when the class should be added

    window.addEventListener("scroll", function () {
        if (window.scrollY > offset) {
            nav.classList.add("sticky-top-right");
        } else {
            nav.classList.remove("sticky-top-right");
        }
    });
});
