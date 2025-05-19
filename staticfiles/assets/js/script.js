const swiper = new Swiper(".home-header .mySwiper", {
    loop: true,
    effect: "fade",
    autoplay: {
        delay: 5000,
        disableOnInteraction: false,
    },
    navigation: {
        nextEl: ".home-header .swiper-button-next",
        prevEl: ".home-header .swiper-button-prev",
    },
    pagination: {
        el: ".home-header .swiper-pagination",
        clickable: true,
    },
});


document.addEventListener('DOMContentLoaded', function () {
    const dropdowns = document.querySelectorAll('.dropdown');
    const dropdownBackground = document.querySelector('.dropdown-background');

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('mouseenter', function () {
            dropdownBackground.style.display = 'block';
            dropdownBackground.style.visibility = 'visible';
            dropdownBackground.style.opacity = '1';
        });

        dropdown.addEventListener('mouseleave', function (e) {
            const relatedTarget = e.relatedTarget;
            if (!dropdown.contains(relatedTarget) && relatedTarget !== dropdownBackground && !dropdownBackground.contains(relatedTarget)) {
                hideDropdownBackground();
            }
        });
    });

    dropdownBackground.addEventListener('mouseleave', function (e) {
        const relatedTarget = e.relatedTarget;
        let isInDropdown = false;

        dropdowns.forEach(dropdown => {
            if (dropdown.contains(relatedTarget)) {
                isInDropdown = true;
            }
        });

        if (!isInDropdown) {
            hideDropdownBackground();
        }
    });

    function hideDropdownBackground() {
        dropdownBackground.style.visibility = 'hidden';
        dropdownBackground.style.opacity = '0';
        setTimeout(() => {
            if (dropdownBackground.style.opacity === '0') {
                dropdownBackground.style.display = 'none';
            }
        }, 100);
    }
});