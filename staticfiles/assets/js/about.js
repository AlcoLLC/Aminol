document.addEventListener("DOMContentLoaded", function () {
  const tabs = document.querySelectorAll(".tab");
  const tabContents = document.querySelectorAll(".tab-content");

  function positionDropletsDynamically(container) {
    const sectionRows = container.querySelectorAll(".section-row");
    const droplets = container.querySelectorAll(".droplet");

    sectionRows.forEach((row, index) => {
      const droplet = droplets[index];
      if (droplet && row) {
        const rowRect = row.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();

        const relativeTop = rowRect.top - containerRect.top;
        const rowHeight = rowRect.height;

        const dropletPosition = relativeTop + rowHeight / 2 - 15;

        droplet.style.top = `${dropletPosition}px`;

        console.log(
          `Droplet ${
            index + 1
          }: Row top: ${relativeTop}px, Row height: ${rowHeight}px, Droplet position: ${dropletPosition}px`
        );
      }
    });
  }

  function positionDropletsForTab(activeTabId) {
    const activeTabContent = document.getElementById(activeTabId);
    if (activeTabContent) {
      const container = activeTabContent.querySelector(
        ".shared-images-container"
      );
      if (container) {
        setTimeout(() => {
          positionDropletsDynamically(container);
        }, 100);
      }
    }
  }

  function positionAllDropletsDynamically() {
    const containers = document.querySelectorAll(".shared-images-container");

    containers.forEach((container) => {
      setTimeout(() => {
        positionDropletsDynamically(container);
      }, 100);
    });
  }

  // Function to get current tab from URL parameter
  function getCurrentTabFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get("tab");
    const validTabs = [
      "about-aminol",
      "quality",
      "production",
      "documents",
      "sustainability",
    ];
    return validTabs.includes(tabParam) ? tabParam : "about-aminol"; // Default to about-aminol
  }

  // Function to update URL without page reload
  function updateUrl(tabId) {
    const urlParams = new URLSearchParams(window.location.search);

    if (tabId === "about-aminol") {
      // Remove tab parameter for default tab to keep URL clean
      urlParams.delete("tab");
    } else {
      urlParams.set("tab", tabId);
    }

    const newUrl =
      window.location.pathname +
      (urlParams.toString() ? "?" + urlParams.toString() : "");
    history.pushState({ tab: tabId }, "", newUrl);
  }

  if (tabs.length > 0) {
    function switchTab(tabId, updateHistory = true) {
      tabContents.forEach((content) => {
        content.classList.remove("active");
      });

      tabs.forEach((tab) => {
        tab.classList.remove("active");
      });

      const selectedContent = document.getElementById(tabId);
      if (selectedContent) {
        selectedContent.classList.add("active");
      }

      const selectedTab = document.querySelector(`[data-tab="${tabId}"]`);
      if (selectedTab) {
        selectedTab.classList.add("active");
      }

      // Update URL if needed
      if (updateHistory) {
        updateUrl(tabId);
      }

      positionDropletsForTab(tabId);
    }

    // Handle tab clicks
    tabs.forEach((tab) => {
      tab.addEventListener("click", function () {
        const tabId = this.getAttribute("data-tab");
        switchTab(tabId, true);
      });
    });

    // Handle browser back/forward buttons
    window.addEventListener("popstate", function (event) {
      const tabId = getCurrentTabFromUrl();
      switchTab(tabId, false); // Don't update history since we're responding to history change
    });

    // Initialize tab based on URL on page load
    const initialTab = getCurrentTabFromUrl();
    switchTab(initialTab, false); // Don't push to history on initial load

    // Position droplets on window resize
    window.addEventListener("resize", function () {
      const activeTab = document.querySelector(".tab.active");
      if (activeTab) {
        const activeTabId = activeTab.getAttribute("data-tab");
        setTimeout(() => {
          positionDropletsForTab(activeTabId);
        }, 200);
      }
    });
  } else {
    positionAllDropletsDynamically();

    window.addEventListener("resize", function () {
      setTimeout(() => {
        positionAllDropletsDynamically();
      }, 200);
    });
  }

  // Position droplets after page fully loads
  window.addEventListener("load", function () {
    if (tabs.length > 0) {
      const activeTab = document.querySelector(".tab.active");
      if (activeTab) {
        const activeTabId = activeTab.getAttribute("data-tab");
        setTimeout(() => {
          positionDropletsForTab(activeTabId);
        }, 300);
      }
    } else {
      setTimeout(() => {
        positionAllDropletsDynamically();
      }, 300);
    }
  });

   const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      // Əgər element ekrana daxil olubsa...
      if (entry.isIntersecting) {
        // 'show' klasını əlavə edərək animasiyanı başladırıq
        entry.target.classList.add('show');
        // Animasiya bir dəfə işlədikdən sonra observer-i dayandırırıq (performans üçün)
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1 // Elementin 10%-i göründükdə animasiya başlasın
  });

  // Bütün .section-row elementlərini seçirik
  const sectionRows = document.querySelectorAll('.section-row');

  sectionRows.forEach((row) => {
    // Sizin HTML kodunuzdakı məntiqə əsasən:
    // Əgər elementdə 'row-reverse' klası varsa, sağdan gəlsin
    if (row.classList.contains('row-reverse')) {
      row.classList.add('from-right');
    } else {
      // Yoxdursa, soldan gəlsin
      row.classList.add('from-left');
    }
    // Hər bir elementi izləməyə başlayırıq
    observer.observe(row);
  });

   const certificationsSwiper = new Swiper('.certifications-carousel', {
    // === Temel Ayarlar ===
    // Slaytların tek tek gösterilmesini sağlar
    slidesPerView: 1, 
    // Slaytlar arası boşluk
    spaceBetween: 30, 
    // Carousel'in sonsuz döngüde çalışmasını sağlar
    loop: true, 

    // === Otomatik Oynatma ===
    autoplay: {
      delay: 5000, // 5 saniyede bir sonraki slayta geçer
      disableOnInteraction: false, // Kullanıcı etkileşiminden sonra durmamasını sağlar
    },

    // === Sayfalama (Noktalar) ===
    pagination: {
      el: '.swiper-pagination',
      clickable: true, // Noktalara tıklanarak geçiş yapılmasını sağlar
    },

    // === İleri/Geri Butonları ===
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  });
  
});
