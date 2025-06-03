document.addEventListener("DOMContentLoaded", function () {
    const cancelBtn = document.querySelector(".page-header .cancel-button");
    const searchInput = document.querySelector(".search-input");
    const searchForm = document.querySelector(".search-form");

    // Cancel button functionality
    if (cancelBtn) {
        cancelBtn.addEventListener("click", function () {
            searchInput.value = "";
            searchInput.focus();
            // Clear results by submitting empty form
            const url = new URL(window.location);
            url.searchParams.delete('search');
            url.searchParams.delete('page');
            window.location.href = url.toString();
        });
    }

    // Auto-submit form on input change (optional - for real-time search)
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener("input", function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                if (searchInput.value.trim().length > 2 || searchInput.value.trim().length === 0) {
                    searchForm.submit();
                }
            }, 500); // Wait 500ms after user stops typing
        });
    }

    // Pagination functionality
    const paginationNumbers = document.querySelectorAll('.page-number');
    const prevBtn = document.getElementById('prevPage');
    const nextBtn = document.getElementById('nextPage');

    // Handle pagination number clicks
    paginationNumbers.forEach(function(pageLink) {
        pageLink.addEventListener('click', function(e) {
            e.preventDefault();
            const pageNum = this.getAttribute('data-page');
            goToPage(pageNum);
        });
    });

    // Handle previous button
    if (prevBtn && !prevBtn.disabled) {
        prevBtn.addEventListener('click', function() {
            const pageNum = this.getAttribute('data-page');
            if (pageNum) {
                goToPage(pageNum);
            }
        });
    }

    // Handle next button
    if (nextBtn && !nextBtn.disabled) {
        nextBtn.addEventListener('click', function() {
            const pageNum = this.getAttribute('data-page');
            if (pageNum) {
                goToPage(pageNum);
            }
        });
    }

    // Function to navigate to specific page
    function goToPage(pageNum) {
        const url = new URL(window.location);
        url.searchParams.set('page', pageNum);
        window.location.href = url.toString();
    }

    // Keyboard navigation for search
    if (searchInput) {
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                searchForm.submit();
            }
            if (e.key === 'Escape') {
                searchInput.value = "";
                searchInput.blur();
            }
        });
    }

    // Focus search input when page loads
    if (searchInput && !searchInput.value) {
        searchInput.focus();
    }

    // Highlight search terms in results (optional enhancement)
    const query = "{{ query|escapejs }}";
    if (query && query.trim()) {
        highlightSearchTerms(query.trim());
    }

    function highlightSearchTerms(searchQuery) {
        const resultContents = document.querySelectorAll('.result-text h2, .result-text .result-description');
        const regex = new RegExp(`(${searchQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        
        resultContents.forEach(function(element) {
            if (element.innerHTML && !element.querySelector('.highlight')) {
                element.innerHTML = element.innerHTML.replace(regex, '<mark class="highlight">$1</mark>');
            }
        });
    }
});