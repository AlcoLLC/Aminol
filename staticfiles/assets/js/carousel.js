const gap = 120;
const itemWidth = 110;
const scrollAmount = itemWidth + gap;
const autoplayDelay = 2700;
const transitionDuration = 1000;

const carousel = document.getElementById("carousel");
const content = document.getElementById("content");
const next = document.getElementById("next");
const prev = document.getElementById("prev");

const cloneContent = content.cloneNode(true);
cloneContent.setAttribute("aria-hidden", "true");
content.appendChild(cloneContent);

let isScrolling = false;
let autoplayTimer;
let startX = 0;
let scrollLeft = 0;
let isDragging = false;

function startAutoplay() {
    autoplayTimer = setInterval(() => {
        if (!isScrolling && !isDragging) {
            moveNext();
        }
    }, autoplayDelay);
}

function stopAutoplay() {
    clearInterval(autoplayTimer);
}

function moveNext() {
    if (isScrolling) return;
    isScrolling = true;

    carousel.style.scrollBehavior = 'smooth';
    carousel.scrollBy({ left: scrollAmount });

    setTimeout(() => {

        if (carousel.scrollLeft >= content.scrollWidth) {
            carousel.style.scrollBehavior = 'auto';
            carousel.scrollLeft = 0;
            carousel.style.scrollBehavior = 'smooth';
        }
        isScrolling = false;
    }, transitionDuration);
}

function movePrev() {
    if (isScrolling) return;
    isScrolling = true;

    carousel.style.scrollBehavior = 'smooth';

    if (carousel.scrollLeft <= 0) {
        carousel.style.scrollBehavior = 'auto';
        carousel.scrollLeft = content.scrollWidth;
        carousel.style.scrollBehavior = 'smooth';
        setTimeout(() => {
            carousel.scrollBy({ left: -scrollAmount });
        }, 10);
    } else {
        carousel.scrollBy({ left: -scrollAmount });
    }

    setTimeout(() => {
        isScrolling = false;
    }, transitionDuration);
}

next.addEventListener("click", () => {
    stopAutoplay();
    moveNext();
    setTimeout(startAutoplay, 1000);
});

prev.addEventListener("click", () => {
    stopAutoplay();
    movePrev();
    setTimeout(startAutoplay, 1000);
});

carousel.addEventListener('mousedown', startDrag);
carousel.addEventListener('touchstart', startDrag, { passive: false });

carousel.addEventListener('mousemove', drag);
carousel.addEventListener('touchmove', drag, { passive: false });

carousel.addEventListener('mouseup', endDrag);
carousel.addEventListener('mouseleave', endDrag);
carousel.addEventListener('touchend', endDrag);

function startDrag(e) {
    isDragging = true;
    stopAutoplay();
    carousel.style.scrollBehavior = 'auto';

    startX = e.type.includes('mouse') ? e.pageX : e.touches[0].pageX;
    scrollLeft = carousel.scrollLeft;

    carousel.style.cursor = 'grabbing';
    e.preventDefault();
}

function drag(e) {
    if (!isDragging) return;
    e.preventDefault();

    const x = e.type.includes('mouse') ? e.pageX : e.touches[0].pageX;
    const walk = (x - startX) * 2;
    carousel.scrollLeft = scrollLeft - walk;
}

function endDrag() {
    if (!isDragging) return;
    isDragging = false;
    carousel.style.cursor = 'grab';
    carousel.style.scrollBehavior = 'smooth';

    setTimeout(() => {
        if (carousel.scrollLeft >= content.scrollWidth) {
            carousel.style.scrollBehavior = 'auto';
            carousel.scrollLeft = 0;
        } else if (carousel.scrollLeft <= 0) {
            carousel.style.scrollBehavior = 'auto';
            carousel.scrollLeft = content.scrollWidth;
        }
        carousel.style.scrollBehavior = 'smooth';
    }, 100);

    setTimeout(startAutoplay, 1000);
}

carousel.addEventListener('mouseenter', stopAutoplay);
carousel.addEventListener('mouseleave', () => {
    if (!isDragging) {
        setTimeout(startAutoplay, 500);
    }
});

document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        stopAutoplay();
    } else {
        setTimeout(startAutoplay, 1000);
    }
});

carousel.style.cursor = 'grab';

startAutoplay();

let ticking = false;
carousel.addEventListener('scroll', () => {
    if (!ticking && !isDragging && !isScrolling) {
        requestAnimationFrame(() => {
            if (carousel.scrollLeft >= content.scrollWidth) {
                carousel.style.scrollBehavior = 'auto';
                carousel.scrollLeft = 0;
                carousel.style.scrollBehavior = 'smooth';
            }
            ticking = false;
        });
        ticking = true;
    }
});