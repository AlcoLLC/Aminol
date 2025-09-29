document.addEventListener("DOMContentLoaded", function () {
  // =================
  // MOBILE MENU FUNCTIONALITY
  // =================
  let isMobileMenuInitialized = false;

  function initializeMobileMenu() {
    if (isMobileMenuInitialized) {
      console.warn(
        "initializeMobileMenu() zaten çalıştırıldı. Tekrar çalıştırılması engellendi."
      );
      return;
    }

    const hamburger = document.getElementById("hamburger");
    const mobileMenu = document.getElementById("mobile-menu");

    if (!hamburger || !mobileMenu) {
      console.error("HATA: Hamburger veya Mobil Menü elementi bulunamadı!");
      return;
    }

    const hamburgerIcon = hamburger.querySelector("i");
    let isProcessingClick = false;

    hamburger.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();

      if (isProcessingClick) {
        return;
      }
      isProcessingClick = true;

      console.log("Hamburger clicked");

      const isActive = mobileMenu.classList.toggle("active");
      hamburger.classList.toggle("active");
      document.body.style.overflow = isActive ? "hidden" : "";

      // Icon değiştirme
      if (hamburgerIcon) {
        hamburgerIcon.className = isActive ? "fas fa-xmark" : "fas fa-bars";
      }

      console.log(
        "Menü durumu değiştirildi. Yeni durum:",
        isActive ? "Açık" : "Kapalı"
      );

      setTimeout(() => {
        isProcessingClick = false;
      }, 200);
    });

    // Menü dışına tıklandığında kapatma
    document.addEventListener("click", function (e) {
      if (
        mobileMenu.classList.contains("active") &&
        !mobileMenu.contains(e.target) &&
        !hamburger.contains(e.target)
      ) {
        mobileMenu.classList.remove("active");
        hamburger.classList.remove("active");
        document.body.style.overflow = "";

        if (hamburgerIcon) {
          hamburgerIcon.className = "fas fa-bars";
        }
      }
    });

    isMobileMenuInitialized = true;
    console.log(
      "✅ Mobile Menu başarıyla yüklendi ve olay dinleyicileri eklendi."
    );
  }

  // =================
  // MOBILE DROPDOWN FUNCTIONALITY
  // =================
  const mobileDropdowns = document.querySelectorAll(".mobile-dropdown");

  mobileDropdowns.forEach((dropdown) => {
    const dropdownHead = dropdown.querySelector(".mobile-dropdown-head");
    const dropdownIcon = dropdown.querySelector("i");

    if (dropdownHead) {
      dropdownHead.addEventListener("click", function (e) {
       if (e.target.tagName.toLowerCase() !== 'a') {
            e.preventDefault();
        } else {
            // Əgər birbaşa linkə kliklənibsə, heç nə etmə və səhifəyə yönlənməsinə icazə ver.
            return; 
        }

        e.stopPropagation();

        const isAlreadyActive = dropdown.classList.contains("active");

        // Önce tüm dropdown'ları kapat
        mobileDropdowns.forEach((d) => {
          d.classList.remove("active");
          const otherIcon = d.querySelector("i");
          if (otherIcon) {
            otherIcon.className = "fa-solid fa-chevron-down";
          }
        });

        // Eğer tıklanan dropdown zaten aktif değilse, onu aktif yap
       if (!isAlreadyActive) {
            dropdown.classList.add("active");
            if (dropdownIcon) {
                dropdownIcon.className = "fa-solid fa-chevron-up";
            }
        } else {
             dropdown.classList.remove("active");
             if (dropdownIcon) {
                dropdownIcon.className = "fa-solid fa-chevron-down";
            }
        }
      });
    }
  });

  // =================
  // DESKTOP DROPDOWN FUNCTIONALITY
  // =================
  const dropdowns = document.querySelectorAll(".dropdown");
  const dropdownBackground = document.querySelector(".dropdown-background");

  if (dropdownBackground) {
    dropdowns.forEach((dropdown) => {
      dropdown.addEventListener("mouseenter", function () {
        // YENİ EKLENEN KOD BAŞLANGICI
        // Üzerine gelinen dropdown'un "products-dropdown" class'ına sahip olup olmadığını kontrol et
        if (this.classList.contains('products-dropdown')) {
          // Eğer evetse, arkaplan yüksekliğini 350px yap
          dropdownBackground.style.height = "300px";
        } else {
          // Değilse, yüksekliği sıfırla (veya varsayılan bir değere ayarla)
          dropdownBackground.style.height = "";
        }
        // YENİ EKLENEN KOD SONU

        dropdownBackground.style.display = "block";
        dropdownBackground.style.visibility = "visible";
        dropdownBackground.style.opacity = "1";
      });

      dropdown.addEventListener("mouseleave", function (e) {
        const relatedTarget = e.relatedTarget;
        if (
          !dropdown.contains(relatedTarget) &&
          relatedTarget !== dropdownBackground &&
          !dropdownBackground.contains(relatedTarget)
        ) {
          hideDropdownBackground();
        }
      });
    });

    dropdownBackground.addEventListener("mouseleave", function (e) {
      const relatedTarget = e.relatedTarget;
      let isInDropdown = false;

      dropdowns.forEach((dropdown) => {
        if (dropdown.contains(relatedTarget)) {
          isInDropdown = true;
        }
      });

      if (!isInDropdown) {
        hideDropdownBackground();
      }
    });
  }

  // Click based dropdown functionality for cases where hover doesn't work
  dropdowns.forEach((dropdown) => {
    const dropdownHead = dropdown.querySelector(".dropdown-head");
    const dropdownContent = dropdown.querySelector(".dropdown-content");

    if (dropdownHead) {
      dropdownHead.addEventListener("click", function (e) {
        // Əgər kliklənən element ox işarəsi (icon) VƏ YA menyu "products-dropdown" DEYİLSƏ,
        // standart davranışı dayandır və menyunu aç/bağla.
        if (e.target.tagName.toLowerCase() === 'i' || !dropdown.classList.contains('products-dropdown')) {
          e.preventDefault();

          // Digər menyuları bağla
          dropdowns.forEach((otherDropdown) => {
            if (otherDropdown !== dropdown) {
              otherDropdown.classList.remove("active");
            }
          });

          // Mövcud menyunu aç/bağla
          dropdown.classList.toggle("active");
        }
        // Əks halda (yəni 'products-dropdown'-a kliklənibsə və bu, icon deyilsə),
        // <a> teqinin standart davranışı (səhifəyə yönləndirmə) işə düşəcək.
      });
    }
  });

  function hideDropdownBackground() {
    if (dropdownBackground) {
      dropdownBackground.style.visibility = "hidden";
      dropdownBackground.style.opacity = "0";
      setTimeout(() => {
        if (dropdownBackground.style.opacity === "0") {
          dropdownBackground.style.display = "none";
        }
      }, 100);
    }
  }

  // =================
  // LANGUAGE DROPDOWN FUNCTIONALITY
  // =================
  // Desktop language dropdown elements
  const langDropdownBtn = document.querySelector(
    ".language-dropdown .lang-dropdown-btn"
  );
  const languageDropdown = document.getElementById("languageDropdown");
  const desktopLangOptions = document.querySelectorAll(
    "#languageDropdown .lang-option"
  );

  // Mobile language dropdown elements
  const mobileLangDropdownBtn = document.querySelector(
    ".mobile-language-dropdown .lang-dropdown-btn"
  );
  const mobileLanguageDropdown = document.getElementById(
    "mobileLanguageDropdown"
  );
  const mobileLangOptions = document.querySelectorAll(
    "#mobileLanguageDropdown .lang-option"
  );

  // Desktop dropdown functionality
  if (langDropdownBtn && languageDropdown) {
    langDropdownBtn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      languageDropdown.classList.toggle("show");
      // Close mobile dropdown if open
      if (mobileLanguageDropdown) {
        mobileLanguageDropdown.classList.remove("show");
      }
    });

    // Close dropdown when clicking outside
    document.addEventListener("click", function (e) {
      if (
        !langDropdownBtn.contains(e.target) &&
        !languageDropdown.contains(e.target)
      ) {
        languageDropdown.classList.remove("show");
      }
    });
  }

  // Mobile language dropdown functionality
  if (mobileLangDropdownBtn && mobileLanguageDropdown) {
    mobileLangDropdownBtn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      mobileLanguageDropdown.classList.toggle("show");
      // Close desktop dropdown if open
      if (languageDropdown) {
        languageDropdown.classList.remove("show");
      }
    });

    // Close dropdown when clicking outside
    document.addEventListener("click", function (e) {
      if (
        !mobileLangDropdownBtn.contains(e.target) &&
        !mobileLanguageDropdown.contains(e.target)
      ) {
        mobileLanguageDropdown.classList.remove("show");
      }
    });
  }

  // Desktop language option click handlers
  desktopLangOptions.forEach((option) => {
    option.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();

      const selectedLang = this.getAttribute("data-lang");

      if (languageDropdown) {
        languageDropdown.classList.remove("show");
      }

      switchLanguage(selectedLang);
    });
  });

  // Mobile language option click handlers
  mobileLangOptions.forEach((option) => {
    option.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();

      const selectedLang = this.getAttribute("data-lang");

      if (mobileLanguageDropdown) {
        mobileLanguageDropdown.classList.remove("show");
      }

      switchLanguage(selectedLang);
    });
  });

  // =================
  // LANGUAGE SWITCHING FUNCTIONS
  // =================
  function switchLanguage(langCode) {
    let csrfValue = getCsrfToken();
    const newPath = calculateNewPath(langCode);

    const currentQueryString = window.location.search;
    const nextUrl = newPath + currentQueryString;

    if (csrfValue) {
      submitLanguageForm(langCode, nextUrl, csrfValue);
    } else {
      window.location.href = nextUrl;
    }
  } 

  function getCsrfToken() {
    // First try meta tag
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta) {
      return csrfMeta.getAttribute("content");
    }

    // Try input field
    const csrfInput = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    );
    if (csrfInput) {
      return csrfInput.value;
    }

    // Try cookie
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split("=");
      if (name === "csrftoken") {
        return value;
      }
    }

    return null;
  }

  function calculateNewPath(langCode) {
    const currentPath = window.location.pathname;
    const supportedLangs = ["az", "de", "fr", "it", "es", "pt-br", "zh-hans"];

    let pathWithoutLang = currentPath;
    let currentLang = "en";

    // Check if current path starts with a language code
    for (let lang of supportedLangs) {
      if (currentPath.startsWith(`/${lang}/`)) {
        currentLang = lang;
        pathWithoutLang = currentPath.substring(lang.length + 1);
        break;
      } else if (currentPath === `/${lang}`) {
        currentLang = lang;
        pathWithoutLang = "/";
        break;
      }
    }

    // Build new path
    if (langCode === "en") {
      return pathWithoutLang;
    } else {
      if (pathWithoutLang === "/") {
        return `/${langCode}/`;
      } else if (pathWithoutLang.startsWith("/")) {
        return `/${langCode}${pathWithoutLang}`;
      } else {
        return `/${langCode}/${pathWithoutLang}`;
      }
    }
  }

  function submitLanguageForm(langCode, nextUrl, csrfToken) {
    const form = document.createElement("form");
    form.method = "POST";
    form.action = "/i18n/setlang/";
    form.style.display = "none";

    const csrfInput = document.createElement("input");
    csrfInput.type = "hidden";
    csrfInput.name = "csrfmiddlewaretoken";
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    const langInput = document.createElement("input");
    langInput.type = "hidden";
    langInput.name = "language";
    langInput.value = langCode;
    form.appendChild(langInput);

    const nextInput = document.createElement("input");
    nextInput.type = "hidden";
    nextInput.name = "next";
    nextInput.value = nextUrl;
    form.appendChild(nextInput);

    document.body.appendChild(form);
    form.submit();
  }

  function setActiveLanguageButton() {
    const currentPath = window.location.pathname;
    let currentLang = "en";

    // Determine current language from URL
    const supportedLangs = ["az", "de", "fr", "it", "es", "pt-br", "zh-hans"];
    for (let lang of supportedLangs) {
      if (currentPath.startsWith(`/${lang}/`) || currentPath === `/${lang}`) {
        currentLang = lang;
        break;
      }
    }

    // Remove active class from all language options
    document.querySelectorAll(".lang-option").forEach((btn) => {
      btn.classList.remove("active");
    });

    // Add active class to current language
    document
      .querySelectorAll(`.lang-option[data-lang="${currentLang}"]`)
      .forEach((btn) => {
        btn.classList.add("active");
      });

    // Update dropdown button text
    const langTexts = {
      en: "EN",
      az: "AZ",
      de: "DE",
      fr: "FR",
      it: "IT",
      es: "ES",
      "pt-br": "PT",
      "zh-hans": "汉语",
    };

    const currentLangText = langTexts[currentLang] || "EN";

    // Update desktop dropdown button
    if (langDropdownBtn) {
      langDropdownBtn.innerHTML = `${currentLangText} <i class="fa-solid fa-angle-down"></i>`;
    }

    // Update mobile dropdown button
    if (mobileLangDropdownBtn) {
      mobileLangDropdownBtn.innerHTML = `${currentLangText} <i class="fa-solid fa-angle-down"></i>`;
    }
  }

  // =================
  // ACTIVE LINKS FUNCTIONALITY
  // =================
  function setActiveLinks() {
    const currentPath = window.location.pathname;
    const allNavLinks = document.querySelectorAll(
      ".navbar a[href], .mobile-menu a[href]"
    );

    // Bütün linklərdən active class-ı sil
    allNavLinks.forEach((link) => {
      link.classList.remove("active");
    });

    const dropdownParents = document.querySelectorAll(
      ".dropdown > a, .mobile-dropdown > .mobile-dropdown-head"
    );
    dropdownParents.forEach((parent) => {
      parent.classList.remove("active");
    });

    // Dropdown linklərini yoxla
    const dropdownLinks = document.querySelectorAll(
      ".dropdown-content a[href], .mobile-dropdown-content a[href]"
    );
    let activeDropdownFound = false;

    dropdownLinks.forEach((dropdownLink) => {
      const linkPath = dropdownLink.getAttribute("href");

      if (
        linkPath === currentPath ||
        (linkPath && linkPath !== "/" && currentPath.startsWith(linkPath))
      ) {
        dropdownLink.classList.add("active");

        const parentDropdown = dropdownLink.closest(".dropdown");
        if (parentDropdown) {
          const parentLink = parentDropdown.querySelector("> a");
          if (parentLink) {
            parentLink.classList.add("active");
            activeDropdownFound = true;
          }
        }

        const parentMobileDropdown = dropdownLink.closest(".mobile-dropdown");
        if (parentMobileDropdown) {
          const parentMobileLink = parentMobileDropdown.querySelector(
            ".mobile-dropdown-head"
          );
          if (parentMobileLink) {
            parentMobileLink.classList.add("active");
            activeDropdownFound = true;
          }
        }
      }
    });

    if (!activeDropdownFound) {
      const regularNavLinks = document.querySelectorAll(
        ".navbar a[href]:not(.dropdown-content a), .mobile-menu a[href]:not(.mobile-dropdown-content a)"
      );

      regularNavLinks.forEach((link) => {
        const linkPath = link.getAttribute("href");

        if (linkPath === currentPath) {
          link.classList.add("active");
        } else if (
          linkPath &&
          linkPath !== "/" &&
          linkPath !== "" &&
          currentPath.startsWith(linkPath)
        ) {
          link.classList.add("active");
        }
      });
    }

    handleSpecialDropdownCases(currentPath);
  }

  function handleSpecialDropdownCases(currentPath) {
    const marketsPaths = [
      "/markets/automotive",
      "/markets/industrial",
      "/markets/shipping",
    ];
    const servicesPaths = [
      "/services/dealer",
      "/services/laboratory",
      "/services/logistics",
    ];

    if (marketsPaths.includes(currentPath)) {
      const marketsDropdown = Array.from(
        document.querySelectorAll(".dropdown > a")
      ).find((link) =>
        link.textContent.trim().toLowerCase().includes("market")
      );

      if (marketsDropdown) {
        marketsDropdown.classList.add("active");
      }

      const mobileMarketsDropdown = Array.from(
        document.querySelectorAll(".mobile-dropdown-head")
      ).find((link) =>
        link.textContent.trim().toLowerCase().includes("market")
      );

      if (mobileMarketsDropdown) {
        mobileMarketsDropdown.classList.add("active");
      }

      const activeDropdownLink = document.querySelector(
        `.dropdown-content a[href="${currentPath}"], .mobile-dropdown-content a[href="${currentPath}"]`
      );
      if (activeDropdownLink) {
        activeDropdownLink.classList.add("active");
      }
    }

    if (servicesPaths.includes(currentPath)) {
      const servicesDropdown = Array.from(
        document.querySelectorAll(".dropdown > a")
      ).find((link) =>
        link.textContent.trim().toLowerCase().includes("service")
      );

      if (servicesDropdown) {
        servicesDropdown.classList.add("active");
      }

      const mobileServicesDropdown = Array.from(
        document.querySelectorAll(".mobile-dropdown-head")
      ).find((link) =>
        link.textContent.trim().toLowerCase().includes("service")
      );

      if (mobileServicesDropdown) {
        mobileServicesDropdown.classList.add("active");
      }

      const activeDropdownLink = document.querySelector(
        `.dropdown-content a[href="${currentPath}"], .mobile-dropdown-content a[href="${currentPath}"]`
      );
      if (activeDropdownLink) {
        activeDropdownLink.classList.add("active");
      }
    }
  }

  initializeMobileMenu();
  setActiveLanguageButton();
  setActiveLinks();

  window.addEventListener("popstate", setActiveLinks);
  window.updateActiveLinks = setActiveLinks;

  window.testLanguageSwitch = function (lang) {
    switchLanguage(lang);
  };

  console.log("Navbar initialized for path:", window.location.pathname);
});
