document.addEventListener("DOMContentLoaded", function () {
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

  // Mobile dropdown functionality
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

  function switchLanguage(langCode) {
    let csrfValue = getCsrfToken();
    const newPath = calculateNewPath(langCode);

    if (csrfValue) {
      submitLanguageForm(langCode, newPath, csrfValue);
    } else {
      window.location.href = newPath;
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
    const supportedLangs = ["az", "de", "fr", "it", "es", "pt", "zh-hans"];

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
    const supportedLangs = ["az", "de", "fr", "it", "es", "pt", "zh-hans"];
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
      pt: "PT",
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

  // Desktop dropdown functionality
  const dropdowns = document.querySelectorAll(".dropdown");
  dropdowns.forEach((dropdown) => {
    const dropdownHead = dropdown.querySelector(".dropdown-head");
    const dropdownContent = dropdown.querySelector(".dropdown-content");

    if (dropdownHead && dropdownContent) {
      dropdownHead.addEventListener("click", function (e) {
        e.preventDefault();

        // Close other dropdowns
        dropdowns.forEach((otherDropdown) => {
          if (otherDropdown !== dropdown) {
            otherDropdown.classList.remove("active");
          }
        });

        // Toggle current dropdown
        dropdown.classList.toggle("active");
      });
    }
  });

  // Mobile menu functionality
  const hamburger = document.getElementById("hamburger");
  const mobileMenu = document.getElementById("mobile-menu");

  if (hamburger && mobileMenu) {
    const hamburgerIcon = hamburger.querySelector("i");

    function openMobileMenu() {
      mobileMenu.classList.add("active");
      if (hamburgerIcon) {
        hamburgerIcon.className = "fa-solid fa-xmark";
      }
      document.body.style.overflow = "hidden";
    }

    function closeMobileMenu() {
      mobileMenu.classList.remove("active");
      if (hamburgerIcon) {
        hamburgerIcon.className = "fas fa-bars";
      }
      document.body.style.overflow = "";
    }

    hamburger.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      if (mobileMenu.classList.contains("active")) {
        closeMobileMenu();
      } else {
        openMobileMenu();
      }
    });

    // Close mobile menu when clicking outside
    document.addEventListener("click", function (e) {
      if (
        mobileMenu.classList.contains("active") &&
        !mobileMenu.contains(e.target) &&
        !hamburger.contains(e.target)
      ) {
        closeMobileMenu();
      }
    });

    // Close on escape key
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && mobileMenu.classList.contains("active")) {
        closeMobileMenu();
      }
    });

    // Close on window resize
    window.addEventListener("resize", function () {
      if (window.innerWidth > 768 && mobileMenu.classList.contains("active")) {
        closeMobileMenu();
      }
    });
  }

  // Mobile dropdown functionality
  const mobileDropdowns = document.querySelectorAll(".mobile-dropdown");
  mobileDropdowns.forEach((dropdown) => {
    const dropdownHead = dropdown.querySelector(".mobile-dropdown-head");
    const dropdownContent = dropdown.querySelector(".mobile-dropdown-content");

    if (dropdownHead && dropdownContent) {
      dropdownHead.addEventListener("click", function (e) {
        e.preventDefault();

        // Close other mobile dropdowns
        mobileDropdowns.forEach((otherDropdown) => {
          if (otherDropdown !== dropdown) {
            otherDropdown.classList.remove("active");
            const otherContent = otherDropdown.querySelector(
              ".mobile-dropdown-content"
            );
            if (otherContent) {
              otherContent.classList.remove("active");
            }
          }
        });

        // Toggle current dropdown
        dropdown.classList.toggle("active");
        dropdownContent.classList.toggle("active");
      });
    }
  });

  // Initialize active language buttons on page load
  setActiveLanguageButton();

  // Test function for debugging
  window.testLanguageSwitch = function (lang) {
    switchLanguage(lang);
  };
});
