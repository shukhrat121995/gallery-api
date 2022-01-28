function navbarToggle() {
    var hamburger = document.getElementById("nav-mobile-id")
    var menu = document.getElementById("nav-menu-id")
    if (hamburger.className === "fas fa-bars") {
        hamburger.className = "fas fa-times"
        menu.className += " active"
    } else {
        hamburger.className = "fas fa-bars"
        menu.className = "nav-menu"
    }
}