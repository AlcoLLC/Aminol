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

    // Checkbox selection highlight
    const checkboxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        const label = checkbox.nextElementSibling;

        if (checkbox.checked) {
            label.classList.add('selected-item');
        }

        checkbox.addEventListener('change', function () {
            if (this.checked) {
                label.classList.add('selected-item');
            } else {
                label.classList.remove('selected-item');
            }
        });
    });

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

    // Pagination functionality
    const prevButton = document.getElementById('prevPage');
    const nextButton = document.getElementById('nextPage');
    const paginationNumbers = document.getElementById('paginationNumbers');
    let currentPage = 1;
    const totalPages = 5; 

    initPagination();

    if (prevButton && nextButton) {
        prevButton.addEventListener('click', function() {
            if (currentPage > 1) {
                navigateToPage(currentPage - 1);
            }
        });

        nextButton.addEventListener('click', function() {
            if (currentPage < totalPages) {
                navigateToPage(currentPage + 1);
            }
        });
    }

    function initPagination() {
        if (!paginationNumbers) return;
        
        updatePaginationUI();
        attachPageNumberListeners();
    }

    function updatePaginationUI() {
        if (!prevButton || !nextButton || !paginationNumbers) return;
        
        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;

        let paginationHTML = '';
        
        for (let i = 1; i <= totalPages; i++) {
            if (
                i === 1 || 
                i === totalPages || 
                i === currentPage || 
                i === currentPage - 1 || 
                i === currentPage + 1
            ) {
                const activeClass = i === currentPage ? 'active' : '';
                paginationHTML += `<a href="#" class="page-number ${activeClass}" data-page="${i}">${i}</a>`;
            } 
            else if (
                (i === currentPage - 2 && currentPage > 3) || 
                (i === currentPage + 2 && currentPage < totalPages - 2)
            ) {
                paginationHTML += `<span class="ellipsis">...</span>`;
            }
        }
        
        paginationNumbers.innerHTML = paginationHTML;
        
        attachPageNumberListeners();
    }

    function attachPageNumberListeners() {
        const pageNumbers = document.querySelectorAll('.page-number');
        pageNumbers.forEach(number => {
            number.addEventListener('click', function(e) {
                e.preventDefault();
                const pageNum = parseInt(this.getAttribute('data-page'));
                navigateToPage(pageNum);
            });
        });
    }

    function navigateToPage(pageNum) {
        if (pageNum < 1 || pageNum > totalPages || pageNum === currentPage) {
            return;
        }

        currentPage = pageNum;
        updatePaginationUI();
        
        loadProductsForPage(currentPage);
    }

    
});