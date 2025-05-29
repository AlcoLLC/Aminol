document.addEventListener('DOMContentLoaded', function() {
    console.log('Language switcher loaded');

    // Bütün dil buttonlarını tapın
    const langButtons = document.querySelectorAll('.btn-az, .btn-en');

    // Hər bir buttona click event əlavə edin
    langButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Language button clicked');

            const selectedLang = this.getAttribute('data-lang');
            console.log('Selected language:', selectedLang);

            switchLanguage(selectedLang);
        });
    });

    // Dil dəyişmə funksiyası
    function switchLanguage(langCode) {
        console.log('Switching to language:', langCode);

        // CSRF token tapın
        const csrfToken = document.querySelector('[name="csrf-token"]') ||
                         document.querySelector('[name="csrfmiddlewaretoken"]') ||
                         document.querySelector('meta[name="csrf-token"]');

        if (!csrfToken) {
            console.error('CSRF token not found');
            return;
        }

        const csrfValue = csrfToken.getAttribute('content') || csrfToken.value;
        console.log('CSRF token found:', csrfValue);

        // Form yaradın
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/i18n/setlang/';
        form.style.display = 'none';

        // CSRF token əlavə edin
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfValue;
        form.appendChild(csrfInput);

        // Language input əlavə edin
        const langInput = document.createElement('input');
        langInput.type = 'hidden';
        langInput.name = 'language';
        langInput.value = langCode;
        form.appendChild(langInput);

        // Next URL əlavə edin
        const nextInput = document.createElement('input');
        nextInput.type = 'hidden';
        nextInput.name = 'next';
        nextInput.value = window.location.pathname;
        form.appendChild(nextInput);

        // Formu body-ə əlavə edin və submit edin
        document.body.appendChild(form);
        console.log('Submitting form...');
        form.submit();
    }
});