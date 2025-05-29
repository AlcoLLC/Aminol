document.addEventListener("DOMContentLoaded", function () {
  console.log("Language switcher loaded");

  // Bütün dil buttonlarını tapın
  const langButtons = document.querySelectorAll(".btn-az, .btn-en");

  // Hər bir buttona click event əlavə edin
  langButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      console.log("Language button clicked");

      const selectedLang = this.getAttribute("data-lang");
      console.log("Selected language:", selectedLang);

      switchLanguage(selectedLang);
    });
  });

  // Dil dəyişmə funksiyası
  function switchLanguage(langCode) {
    console.log("Switching to language:", langCode);

    // CSRF token tapın - müxtəlif yerlərdən
    let csrfValue = null;

    // Method 1: Meta tag-dən (ən etibarlı)
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta) {
      csrfValue = csrfMeta.getAttribute("content");
    }

    // Method 2: Django template-dən gizli input
    if (!csrfValue) {
      const csrfTokenInput = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      );
      if (csrfTokenInput) {
        csrfValue = csrfTokenInput.value;
      }
    }

    // Method 3: Cookie-dən
    if (!csrfValue) {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        const [name, value] = cookie.trim().split("=");
        if (name === "csrftoken") {
          csrfValue = value;
          break;
        }
      }
    }

    console.log("CSRF token found:", csrfValue ? "Yes" : "No");

    // Hal-hazırkı URL-i təhlil edin
    const currentPath = window.location.pathname;
    let newPath = currentPath;

    // URL-də dil prefixini düzgün idarə edin
    if (currentPath.startsWith("/az/")) {
      newPath = currentPath.substring(3); // /az/ prefixini çıxarın
    } else if (currentPath.startsWith("/en/")) {
      newPath = currentPath.substring(3); // /en/ prefixini çıxarın
    } else if (currentPath === "/az" || currentPath === "/en") {
      newPath = "/";
    }

    // Yeni dil prefixini əlavə edin
    if (langCode === "az") {
      newPath = `/az${newPath}`;
    } else {
      // EN default dildir, prefix əlavə etmirik
      newPath = newPath === "" ? "/" : newPath;
    }

    // Əgər CSRF token varsa, form submit edin
    if (csrfValue) {
      // Form yaradın
      const form = document.createElement("form");
      form.method = "POST";
      form.action = "/i18n/setlang/";
      form.style.display = "none";

      // CSRF token əlavə edin
      const csrfInput = document.createElement("input");
      csrfInput.type = "hidden";
      csrfInput.name = "csrfmiddlewaretoken";
      csrfInput.value = csrfValue;
      form.appendChild(csrfInput);

      // Language input əlavə edin
      const langInput = document.createElement("input");
      langInput.type = "hidden";
      langInput.name = "language";
      langInput.value = langCode;
      form.appendChild(langInput);

      // Next URL əlavə edin
      const nextInput = document.createElement("input");
      nextInput.type = "hidden";
      nextInput.name = "next";
      nextInput.value = newPath;
      form.appendChild(nextInput);

      // Form-u səhifəyə əlavə edin və submit edin
      document.body.appendChild(form);
      form.submit();
    } else {
      // CSRF token yoxdursa, sadəcə redirect edin
      console.warn("CSRF token not found, using simple redirect");
      window.location.href = newPath;
    }
  }

  // Aktiv dil buttonunu təyin edin
  function setActiveLanguageButton() {
    const currentPath = window.location.pathname;
    let currentLang = "en"; // default

    if (currentPath.startsWith("/az/") || currentPath === "/az") {
      currentLang = "az";
    }

    // Bütün buttonları passiv edin
    langButtons.forEach((btn) => {
      btn.classList.remove("active");
    });

    // Aktiv dili işarələyin
    const activeButtons = document.querySelectorAll(
      `[data-lang="${currentLang}"]`
    );
    activeButtons.forEach((btn) => {
      btn.classList.add("active");
    });
  }

  // Səhifə yüklənəndə aktiv dili təyin edin
  setActiveLanguageButton();
});
