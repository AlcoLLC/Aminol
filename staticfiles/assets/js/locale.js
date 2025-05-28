// Language switching functionality
document.addEventListener('DOMContentLoaded', function() {
    const langButtons = document.querySelectorAll('[data-lang]');
    const currentLang = document.documentElement.lang || 'en';
    
    // Set initial active state based on current language
    updateButtonStates(currentLang);
    
    // Add click event listeners to all language buttons
    langButtons.forEach(button => {
        button.addEventListener('click', function() {
            const selectedLang = this.getAttribute('data-lang');
            switchLanguage(selectedLang);
        });
    });
    
    function switchLanguage(lang) {
        // Create form and submit to Django's set_language view
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/i18n/setlang/';
        form.style.display = 'none';
        
        // Add CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrfToken.value;
            form.appendChild(csrfInput);
        }
        
        // Add language input
        const langInput = document.createElement('input');
        langInput.type = 'hidden';
        langInput.name = 'language';
        langInput.value = lang;
        form.appendChild(langInput);
        
        // Add next URL to redirect back to current page
        const nextInput = document.createElement('input');
        nextInput.type = 'hidden';
        nextInput.name = 'next';
        nextInput.value = window.location.pathname;
        form.appendChild(nextInput);
        
        document.body.appendChild(form);
        form.submit();
    }
    
    function updateButtonStates(activeLang) {
        // Reset all buttons
        const azButtons = document.querySelectorAll('[data-lang="az"]');
        const enButtons = document.querySelectorAll('[data-lang="en"]');
        
        azButtons.forEach(btn => {
            btn.classList.remove('active');
            btn.style.backgroundColor = 'transparent';
            btn.style.color = '#012762';
            btn.style.border = 'none';
        });
        
        enButtons.forEach(btn => {
            btn.classList.remove('active');
            btn.style.backgroundColor = 'transparent';
            btn.style.color = '#012762';
            btn.style.border = 'none';
        });
        
        // Set active button style
        const activeButtons = document.querySelectorAll(`[data-lang="${activeLang}"]`);
        activeButtons.forEach(btn => {
            btn.classList.add('active');
            btn.style.backgroundColor = '#012762';
            btn.style.color = '#fff';
            btn.style.border = '1px solid #fff';
            btn.style.borderRadius = '12px';
            btn.style.padding = '2px 10px';
        });
        
        // Set inactive button style
        const inactiveButtons = document.querySelectorAll(`[data-lang="${activeLang === 'az' ? 'en' : 'az'}"]`);
        inactiveButtons.forEach(btn => {
            btn.style.padding = activeLang === 'az' ? '2px 10px' : '0 6px 0 8px';
        });
    }
});