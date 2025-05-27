
const gap = 120;
const itemWidth = 110;
const scrollAmount = itemWidth + gap;
const autoplayDelay = 2700;
const transitionDuration = 800;

const carousel = document.getElementById("carousel2");
const content = document.getElementById("content2");
const next = document.getElementById("next2");
const prev = document.getElementById("prev2");

const originalContent = content.innerHTML;
content.innerHTML = originalContent + originalContent + originalContent;

let isScrolling = false;
let autoplayTimer;
let startX = 0;
let scrollLeft = 0;
let isDragging = false;

 
const totalWidth = content.scrollWidth / 3;
carousel.scrollLeft = totalWidth;

function startAutoplay() {
    clearInterval(autoplayTimer);
    autoplayTimer = setInterval(() => {
        if (!isScrolling && !isDragging) {
            moveNext();
        }
    }, autoplayDelay);
}

function stopAutoplay() {
    clearInterval(autoplayTimer);
}

function checkPosition() {
    const totalWidth = content.scrollWidth / 3;
    
    if (carousel.scrollLeft >= totalWidth * 2) {
        carousel.style.scrollBehavior = 'auto';
        carousel.scrollLeft = totalWidth;
        setTimeout(() => {
            carousel.style.scrollBehavior = 'smooth';
        }, 10);
    } else if (carousel.scrollLeft <= 0) {
        carousel.style.scrollBehavior = 'auto';
        carousel.scrollLeft = totalWidth;
        setTimeout(() => {
            carousel.style.scrollBehavior = 'smooth';
        }, 10);
    }
}

function moveNext() {
    if (isScrolling) return;
    isScrolling = true;

    carousel.style.scrollBehavior = 'smooth';
    carousel.scrollBy({ left: scrollAmount });

    setTimeout(() => {
        checkPosition();
        isScrolling = false;
    }, transitionDuration);
}

function movePrev() {
    if (isScrolling) return;
    isScrolling = true;

    carousel.style.scrollBehavior = 'smooth';
    carousel.scrollBy({ left: -scrollAmount });

    setTimeout(() => {
        checkPosition();
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

// Drag functionality
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
    const walk = (x - startX) * 1.5;
    carousel.scrollLeft = scrollLeft - walk;
}

function endDrag() {
    if (!isDragging) return;
    isDragging = false;
    carousel.style.cursor = 'grab';
    carousel.style.scrollBehavior = 'smooth';

    setTimeout(() => {
        checkPosition();
    }, 100);

    setTimeout(startAutoplay, 1500);
}

// Mouse hover pause
carousel.addEventListener('mouseenter', stopAutoplay);
carousel.addEventListener('mouseleave', () => {
    if (!isDragging) {
        setTimeout(startAutoplay, 500);
    }
});

// Page visibility
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        stopAutoplay();
    } else {
        setTimeout(startAutoplay, 1000);
    }
});

// Scroll event for smooth infinite loop
let scrollTimeout;
carousel.addEventListener('scroll', () => {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
        if (!isDragging && !isScrolling) {
            checkPosition();
        }
    }, 150);
});

// Initialize
carousel.style.cursor = 'grab';
carousel.style.scrollBehavior = 'auto';
carousel.scrollLeft = totalWidth;
carousel.style.scrollBehavior = 'smooth';

setTimeout(startAutoplay, 1000);