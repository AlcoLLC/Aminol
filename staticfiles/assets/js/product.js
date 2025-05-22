document.addEventListener('DOMContentLoaded', function () {
    // Filter header toggle functionality
    const filterHeaders = document.querySelectorAll('.filter-header');

    filterHeaders.forEach(header => {
        header.addEventListener('click', function () {
            this.classList.toggle('active');
            const content = this.nextElementSibling;
            content.classList.toggle('open');
            const icon = this.querySelector('.filter-icon i');
            if (content.classList.contains('open')) {
                icon.classList.remove('fa-chevron-down');
                icon.classList.add('fa-chevron-up');
            } else {
                icon.classList.remove('fa-chevron-up');
                icon.classList.add('fa-chevron-down');
            }
        });
    });

    // Auto-submit form when filters change
    const checkboxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]');
    const searchInput = document.querySelector('input[name="search"]');
    
    checkboxes.forEach(checkbox => {
        const label = checkbox.nextElementSibling;
        
        checkbox.addEventListener('change', function () {
            if (this.checked) {
                label.classList.add('selected-item');
            } else {
                label.classList.remove('selected-item');
            }
            // Reset to page 1 when filtering
            const pageInput = document.querySelector('input[name="page"]');
            if (pageInput) {
                pageInput.value = 1;
            }
            const form = document.getElementById('filterForm');
            if (form) {
                form.submit();
            }
        });
    });

    // Search input - only submit on Enter key press
    if (searchInput) {
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Prevent default form submission
                const pageInput = document.querySelector('input[name="page"]');
                if (pageInput) {
                    pageInput.value = 1;
                }
                const form = document.getElementById('filterForm');
                if (form) {
                    form.submit();
                }
            }
        });
    }

    // Search button click handler
    const searchButton = document.querySelector('.search-button');
    if (searchButton) {
        searchButton.addEventListener('click', function(e) {
            e.preventDefault();
            const pageInput = document.querySelector('input[name="page"]');
            if (pageInput) {
                pageInput.value = 1;
            }
            const form = document.getElementById('filterForm');
            if (form) {
                form.submit();
            }
        });
    }

    // Pagination functionality
    const prevButton = document.getElementById('prevPage');
    const nextButton = document.getElementById('nextPage');
    const pageNumbers = document.querySelectorAll('.page-number');
    
    if (prevButton) {
        prevButton.addEventListener('click', function() {
            if (!this.disabled) {
                const currentPageSpan = document.querySelector('.page-number.active');
                if (currentPageSpan) {
                    const currentPage = parseInt(currentPageSpan.getAttribute('data-page'));
                    if (currentPage > 1) {
                        navigateToPage(currentPage - 1);
                    }
                }
            }
        });
    }

    if (nextButton) {
        nextButton.addEventListener('click', function() {
            if (!this.disabled) {
                const currentPageSpan = document.querySelector('.page-number.active');
                if (currentPageSpan) {
                    const currentPage = parseInt(currentPageSpan.getAttribute('data-page'));
                    navigateToPage(currentPage + 1);
                }
            }
        });
    }

    pageNumbers.forEach(number => {
        number.addEventListener('click', function(e) {
            e.preventDefault();
            const pageNum = parseInt(this.getAttribute('data-page'));
            if (pageNum) {
                navigateToPage(pageNum);
            }
        });
    });

    function navigateToPage(pageNum) {
        const form = document.getElementById('filterForm');
        const pageInput = document.querySelector('input[name="page"]');
        if (pageInput && form) {
            pageInput.value = pageNum;
            form.submit();
        }
    }

    // Animation on scroll for sections
    checkScroll();
    window.addEventListener("scroll", checkScroll);

    function checkScroll() {
        const sections = document.querySelectorAll(".section");
        sections.forEach((section) => {
            const sectionTop = section.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            if (sectionTop < windowHeight * 0.85) {
                section.classList.add("active");
            } else {
                section.classList.remove("active");
            }
        });
    }
});