// Language switching functionality
document.addEventListener('DOMContentLoaded', function () {
  // Get current language from URL or default to 'en'
  const currentPath = window.location.pathname;
  const currentLang = currentPath.startsWith('/az/') ? 'az' : 'en';

  // Set initial active state based on current language
  updateButtonStates(currentLang);

  // Add click event listeners to all language buttons
  const langButtons = document.querySelectorAll('.btn-az, .btn-en');

  langButtons.forEach((button) => {
    button.addEventListener('click', function (e) {
      e.preventDefault();
      const selectedLang = this.getAttribute('data-lang');
      if (selectedLang !== currentLang) {
        switchLanguage(selectedLang);
      }
    });
  });

  function switchLanguage(lang) {
    const currentPath = window.location.pathname;
    let newPath;

    if (lang === 'az') {
      // Switch to Azerbaijani
      if (currentPath.startsWith('/az/')) {
        newPath = currentPath; // Already in AZ
      } else {
        newPath = '/az' + (currentPath === '/' ? '/' : currentPath);
      }
    } else {
      // Switch to English
      if (currentPath.startsWith('/az/')) {
        newPath = currentPath.substring(3) || '/';
      } else {
        newPath = currentPath; // Already in EN
      }
    }

    window.location.href = newPath;
  }

  function updateButtonStates(activeLang) {
    // Get all language buttons
    const azButtons = document.querySelectorAll('.btn-az');
    const enButtons = document.querySelectorAll('.btn-en');

    // Reset all buttons to inactive state
    azButtons.forEach((btn) => {
      btn.classList.remove('active');
      btn.style.cssText = '';
    });

    enButtons.forEach((btn) => {
      btn.classList.remove('active');
      btn.style.cssText = '';
    });

    // Set active button style
    if (activeLang === '/az') {
      azButtons.forEach((btn) => {
        btn.classList.add('active');
        btn.style.cssText =
          'background-color: #012762 !important; color: #fff !important; border: 1px solid #fff !important; border-radius: 12px !important; padding: 2px 10px !important;';
      });
      enButtons.forEach((btn) => {
        btn.style.cssText =
          'background-color: transparent !important; color: #012762 !important; border: none !important; padding: 2px 10px !important;';
      });
    } else {
      enButtons.forEach((btn) => {
        btn.classList.add('active');
        btn.style.cssText =
          'background-color: #012762 !important; color: #fff !important; border: 1px solid #fff !important; border-radius: 12px !important; padding: 2px 10px !important;';
      });
      azButtons.forEach((btn) => {
        btn.style.cssText =
          'background-color: transparent !important; color: #012762 !important; border: none !important; padding: 0 6px 0 8px !important;';
      });
    }
  }
});
