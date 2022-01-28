function handleScroll() {
    var sb = document.getElementById("scroll-bar-id")
    var ra = document.getElementById("arrow-right-id")
    var la = document.getElementById("arrow-left-id")
    var bottom = sb.scrollWidth - sb.scrollLeft < sb.clientWidth + 1
    if (bottom) {
        ra.style.visibility = 'hidden'
    } else {
        ra.style.visibility = 'visible'
    }
    if (sb.scrollLeft === 0) {
        la.style.visibility = 'hidden'
    } else {
        la.style.visibility = 'visible'
    }
}

function scrollBar(direction) {
    var sb = document.getElementById("scroll-bar-id")
    sb.style.scrollBehavior = 'smooth';
    if (direction === 'left') {
        sb.scrollLeft -= 200
    } else {
        sb.scrollLeft += 200
    }
}