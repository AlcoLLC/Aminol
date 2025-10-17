document.addEventListener("DOMContentLoaded", function () {
  const filterHeaders = document.querySelectorAll(".filter-header");
  filterHeaders.forEach((header) => {
    header.addEventListener("click", function () {
      this.classList.toggle("active");
      const content = this.nextElementSibling;
      content.classList.toggle("open");
      const icon = this.querySelector(".filter-icon i");
      if (content.classList.contains("open")) {
        icon.classList.remove("fa-chevron-down");
        icon.classList.add("fa-chevron-up");
      } else {
        icon.classList.remove("fa-chevron-up");
        icon.classList.add("fa-chevron-down");
      }
    });
  });
  const desktopCheckboxes = document.querySelectorAll(
    '.filter-container .checkbox-group input[type="checkbox"]'
  );
  const searchInput = document.querySelector(
    '.filter-container input[name="search"]'
  );

  desktopCheckboxes.forEach((checkbox) => {
    const label = checkbox.nextElementSibling;

    checkbox.addEventListener("change", function () {
      if (this.checked) {
        label.classList.add("selected-item");
      } else {
        label.classList.remove("selected-item");
      }
    });
  });
  if (searchInput) {
    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        handleSearchSubmit();
      }
    });
  }
  const searchButton = document.querySelector(
    ".filter-container .search-button"
  );
  if (searchButton) {
    searchButton.addEventListener("click", function (e) {
      e.preventDefault();
      handleSearchSubmit();
    });
  }
  const filterResultsBtn = document.getElementById("filterResultsBtn");
  if (filterResultsBtn) {
    filterResultsBtn.addEventListener("click", function () {
      handleFilterSubmit();
    });
  }
  function handleSearchSubmit() {
    const searchInput = document.querySelector(
      '.filter-container input[name="search"]'
    );
    const searchTerm = searchInput.value.trim();

    if (searchTerm) {
      const searchUrl = `/products/search/${encodeURIComponent(searchTerm)}/`;
      window.location.href = searchUrl;
    } else {
      handleFilterSubmit();
    }
  }
  function handleFilterSubmit() {
    const selectedFilters = getSelectedFilters();
    const seoUrl = generateSeoFriendlyUrl(selectedFilters);
    if (seoUrl) {
      window.location.href = seoUrl;
    } else {
      window.location.href = "/products/";
    }
  }
  function getSelectedFilters() {
    const form = document.getElementById("filterForm");
    const filters = {
      product_groups: [],
      segments: [],
      oil_types: [],
      viscosities: [],
    };
    const productGroupCheckboxes = form.querySelectorAll(
      'input[name="product_group"]:checked'
    );
    const segmentCheckboxes = form.querySelectorAll(
      'input[name="segments"]:checked'
    );
    const oilTypeCheckboxes = form.querySelectorAll(
      'input[name="oil_type"]:checked'
    );
    const viscosityCheckboxes = form.querySelectorAll(
      'input[name="viscosity"]:checked'
    );
    productGroupCheckboxes.forEach((cb) =>
      filters.product_groups.push(cb.value)
    );
    segmentCheckboxes.forEach((cb) => filters.segments.push(cb.value));
    oilTypeCheckboxes.forEach((cb) => filters.oil_types.push(cb.value));
    viscosityCheckboxes.forEach((cb) => filters.viscosities.push(cb.value));

    return filters;
  }
  function generateSeoFriendlyUrl(filters) {
    const { product_groups, segments, oil_types, viscosities } = filters;
    if (
      product_groups.length === 1 &&
      segments.length === 0 &&
      oil_types.length === 0 &&
      viscosities.length === 0
    ) {
      return `/products/category/${product_groups[0]}/`;
    }
    if (
      segments.length === 1 &&
      product_groups.length === 0 &&
      oil_types.length === 0 &&
      viscosities.length === 0
    ) {
      return `/products/segment/${segments[0]}/`;
    }
    if (
      oil_types.length === 1 &&
      product_groups.length === 0 &&
      segments.length === 0 &&
      viscosities.length === 0
    ) {
      return `/products/oil-type/${oil_types[0]}/`;
    }
    if (
      viscosities.length === 1 &&
      product_groups.length === 0 &&
      segments.length === 0 &&
      oil_types.length === 0
    ) {
      return `/products/viscosity/${viscosities[0]}/`;
    }
    if (
      product_groups.length === 1 &&
      segments.length === 1 &&
      oil_types.length === 0 &&
      viscosities.length === 0
    ) {
      return `/products/category/${product_groups[0]}/${segments[0]}/`;
    }
    if (
      product_groups.length === 1 &&
      oil_types.length === 1 &&
      segments.length === 0 &&
      viscosities.length === 0
    ) {
      return `/products/category/${product_groups[0]}/oil-type/${oil_types[0]}/`;
    }
    if (
      product_groups.length === 1 &&
      viscosities.length === 1 &&
      segments.length === 0 &&
      oil_types.length === 0
    ) {
      return `/products/category/${product_groups[0]}/viscosity/${viscosities[0]}/`;
    }
    if (
      segments.length === 1 &&
      oil_types.length === 1 &&
      product_groups.length === 0 &&
      viscosities.length === 0
    ) {
      return `/products/segment/${segments[0]}/oil-type/${oil_types[0]}/`;
    }
    if (
      segments.length === 1 &&
      viscosities.length === 1 &&
      product_groups.length === 0 &&
      oil_types.length === 0
    ) {
      return `/products/segment/${segments[0]}/viscosity/${viscosities[0]}/`;
    }
    if (
      product_groups.length > 0 ||
      segments.length > 0 ||
      oil_types.length > 0 ||
      viscosities.length > 0
    ) {
      let queryParams = [];

      if (product_groups.length > 0) {
        product_groups.forEach((group) =>
          queryParams.push(`product_group=${group}`)
        );
      }
      if (segments.length > 0) {
        segments.forEach((segment) => queryParams.push(`segments=${segment}`));
      }
      if (oil_types.length > 0) {
        oil_types.forEach((oil_type) =>
          queryParams.push(`oil_type=${oil_type}`)
        );
      }
      if (viscosities.length > 0) {
        viscosities.forEach((viscosity) =>
          queryParams.push(`viscosity=${viscosity}`)
        );
      }
      return `/products/?${queryParams.join("&")}`;
    }
    return "/products/";
  }
  const prevButton = document.getElementById("prevPage");
  const nextButton = document.getElementById("nextPage");
  const pageNumbers = document.querySelectorAll(".page-number");
  if (prevButton) {
    prevButton.addEventListener("click", function () {
      if (!this.disabled) {
        const currentPageSpan = document.querySelector(".page-number.active");
        if (currentPageSpan) {
          const currentPage = parseInt(
            currentPageSpan.getAttribute("data-page")
          );
          if (currentPage > 1) {
            navigateToPage(currentPage - 1);
          }
        }
      }
    });
  }
  if (nextButton) {
    nextButton.addEventListener("click", function () {
      if (!this.disabled) {
        const currentPageSpan = document.querySelector(".page-number.active");
        if (currentPageSpan) {
          const currentPage = parseInt(
            currentPageSpan.getAttribute("data-page")
          );
          navigateToPage(currentPage + 1);
        }
      }
    });
  }
  pageNumbers.forEach((number) => {
    number.addEventListener("click", function (e) {
      e.preventDefault();
      const pageNum = parseInt(this.getAttribute("data-page"));
      if (pageNum) {
        navigateToPage(pageNum);
      }
    });
  });
  function navigateToPage(pageNum) {
    const currentUrl = window.location.pathname;
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set("page", pageNum);
    const newUrl = `${currentUrl}?${urlParams.toString()}`;

    window.location.href = newUrl;
  }
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
document.addEventListener("DOMContentLoaded", function () {
  const mobileFilterBtn = document.getElementById("filterMobileBtn");
  const productFilterModal = document.getElementById("productFilterModal");
  const productModalClose = document.getElementById("productModalClose");
  const productSearchResultsBtn = document.getElementById(
    "productSearchResultsBtn"
  );
  if (mobileFilterBtn) {
    mobileFilterBtn.addEventListener("click", function () {
      productFilterModal.classList.add("show-modal");
      document.body.style.overflow = "hidden";
    });
  }

  // Close modal function
  function closeProductModal() {
    productFilterModal.classList.remove("show-modal");
    document.body.style.overflow = "auto";
  }

  // Close modal button
  if (productModalClose) {
    productModalClose.addEventListener("click", closeProductModal);
  }

  // Close modal when clicking overlay
  if (productFilterModal) {
    productFilterModal.addEventListener("click", function (e) {
      if (e.target === productFilterModal) {
        closeProductModal();
      }
    });
  }
  document.addEventListener("keydown", function (e) {
    if (
      e.key === "Escape" &&
      productFilterModal.classList.contains("show-modal")
    ) {
      closeProductModal();
    }
  });
  const modalFilterHeaders = document.querySelectorAll(".modal-filter-header");
  modalFilterHeaders.forEach((header) => {
    header.addEventListener("click", function () {
      const currentContent = this.nextElementSibling;
      const currentIcon = this.querySelector(".modal-filter-icon i");
      const isCurrentlyOpen =
        currentContent.classList.contains("modal-content-open");
      modalFilterHeaders.forEach((otherHeader) => {
        if (otherHeader !== this) {
          const otherContent = otherHeader.nextElementSibling;
          const otherIcon = otherHeader.querySelector(".modal-filter-icon i");

          otherHeader.classList.remove("modal-header-active");
          otherContent.classList.remove("modal-content-open");
          otherIcon.classList.remove("fa-chevron-up");
          otherIcon.classList.add("fa-chevron-down");
        }
      });
      if (!isCurrentlyOpen) {
        this.classList.add("modal-header-active");
        currentContent.classList.add("modal-content-open");
        currentIcon.classList.remove("fa-chevron-down");
        currentIcon.classList.add("fa-chevron-up");
      } else {
        this.classList.remove("modal-header-active");
        currentContent.classList.remove("modal-content-open");
        currentIcon.classList.remove("fa-chevron-up");
        currentIcon.classList.add("fa-chevron-down");
      }
    });
  });
  const modalCheckboxes = document.querySelectorAll(
    '.modal-checkbox-group input[type="checkbox"]'
  );
  modalCheckboxes.forEach((checkbox) => {
    const label = checkbox.nextElementSibling;
    checkbox.addEventListener("change", function () {
      if (this.checked) {
        label.classList.add("modal-selected-item");
      } else {
        label.classList.remove("modal-selected-item");
      }
    });
  });
  function getModalSelectedFilters() {
    const modalForm = document.getElementById("modalFilterForm");
    const filters = {
      product_groups: [],
      segments: [],
      oil_types: [],
      viscosities: [],
    };
    const productGroupCheckboxes = modalForm.querySelectorAll(
      'input[name="product_group"]:checked'
    );
    const segmentCheckboxes = modalForm.querySelectorAll(
      'input[name="segments"]:checked'
    );
    const oilTypeCheckboxes = modalForm.querySelectorAll(
      'input[name="oil_type"]:checked'
    );
    const viscosityCheckboxes = modalForm.querySelectorAll(
      'input[name="viscosity"]:checked'
    );
    productGroupCheckboxes.forEach((cb) =>
      filters.product_groups.push(cb.value)
    );
    segmentCheckboxes.forEach((cb) => filters.segments.push(cb.value));
    oilTypeCheckboxes.forEach((cb) => filters.oil_types.push(cb.value));
    viscosityCheckboxes.forEach((cb) => filters.viscosities.push(cb.value));

    return filters;
  }
  function generateModalSeoFriendlyUrl(filters) {
    const { product_groups, segments, oil_types, viscosities } = filters;

    if (
      product_groups.length === 1 &&
      segments.length === 0 &&
      oil_types.length === 0 &&
      viscosities.length === 0
    ) {
      return `/products/category/${product_groups[0]}/`;
    }
    if (
      segments.length === 1 &&
      product_groups.length === 0 &&
      oil_types.length === 0 &&
      viscosities.length === 0
    ) {
      return `/products/segment/${segments[0]}/`;
    }
    if (
      oil_types.length === 1 &&
      product_groups.length === 0 &&
      segments.length === 0 &&
      viscosities.length === 0
    ) {
      return `/products/oil-type/${oil_types[0]}/`;
    }
    if (
      viscosities.length === 1 &&
      product_groups.length === 0 &&
      segments.length === 0 &&
      oil_types.length === 0
    ) {
      return `/products/viscosity/${viscosities[0]}/`;
    }
    if (
      product_groups.length === 1 &&
      segments.length === 1 &&
      oil_types.length === 0 &&
      viscosities.length === 0
    ) {
      return `/products/category/${product_groups[0]}/${segments[0]}/`;
    }
    if (
      product_groups.length === 1 &&
      oil_types.length === 1 &&
      segments.length === 0 &&
      viscosities.length === 0
    ) {
      return `/products/category/${product_groups[0]}/oil-type/${oil_types[0]}/`;
    }
    if (
      product_groups.length === 1 &&
      viscosities.length === 1 &&
      segments.length === 0 &&
      oil_types.length === 0
    ) {
      return `/products/category/${product_groups[0]}/viscosity/${viscosities[0]}/`;
    }
    if (
      segments.length === 1 &&
      oil_types.length === 1 &&
      product_groups.length === 0 &&
      viscosities.length === 0
    ) {
      return `/products/segment/${segments[0]}/oil-type/${oil_types[0]}/`;
    }
    if (
      segments.length === 1 &&
      viscosities.length === 1 &&
      product_groups.length === 0 &&
      oil_types.length === 0
    ) {
      return `/products/segment/${segments[0]}/viscosity/${viscosities[0]}/`;
    }
    if (
      product_groups.length > 0 ||
      segments.length > 0 ||
      oil_types.length > 0 ||
      viscosities.length > 0
    ) {
      let queryParams = [];
      if (product_groups.length > 0) {
        product_groups.forEach((group) =>
          queryParams.push(`product_group=${group}`)
        );
      }
      if (segments.length > 0) {
        segments.forEach((segment) => queryParams.push(`segments=${segment}`));
      }
      if (oil_types.length > 0) {
        oil_types.forEach((oil_type) =>
          queryParams.push(`oil_type=${oil_type}`)
        );
      }
      if (viscosities.length > 0) {
        viscosities.forEach((viscosity) =>
          queryParams.push(`viscosity=${viscosity}`)
        );
      }
      return `/products/?${queryParams.join("&")}`;
    }
    return "/products/";
  }
  if (productSearchResultsBtn) {
    productSearchResultsBtn.addEventListener("click", function () {
      const modalSearchInput = document.querySelector(".modal-search-input");
      const searchTerm = modalSearchInput ? modalSearchInput.value.trim() : "";
      if (searchTerm) {
        const searchUrl = `/products/search/${encodeURIComponent(searchTerm)}/`;
        window.location.href = searchUrl;
      } else {
        const selectedFilters = getModalSelectedFilters();
        const seoUrl = generateModalSeoFriendlyUrl(selectedFilters);
        window.location.href = seoUrl;
      }
      closeProductModal();
    });
  }

  const modalSearchButton = document.querySelector(".modal-search-button");
  const modalSearchInput = document.querySelector(".modal-search-input");
  if (modalSearchButton) {
    modalSearchButton.addEventListener("click", function () {
      const searchTerm = modalSearchInput ? modalSearchInput.value.trim() : "";
      if (searchTerm) {
        const searchUrl = `/products/search/${encodeURIComponent(searchTerm)}/`;
        window.location.href = searchUrl;
        closeProductModal();
      } else {
        if (productSearchResultsBtn) {
          productSearchResultsBtn.click();
        }
      }
    });
  }
  if (modalSearchInput) {
    modalSearchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        const searchTerm = this.value.trim();
        if (searchTerm) {
          const searchUrl = `/products/search/${encodeURIComponent(
            searchTerm
          )}/`;
          window.location.href = searchUrl;
          closeProductModal();
        } else {
          if (productSearchResultsBtn) {
            productSearchResultsBtn.click();
          }
        }
      }
    });
  }
});
