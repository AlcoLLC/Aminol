document.addEventListener('DOMContentLoaded', function () {
    const customSelect = document.querySelector('.custom-select');
    const customOptions = document.querySelector('.custom-options');
    const optionItems = document.querySelectorAll('.custom-option');
    const hiddenInput = document.querySelector('#helpType');
    const contactForm = document.querySelector('form[action*="contact"]');
   
    if (!customSelect || !customOptions) {
        console.error("Custom select elements not found!");
        return;
    }
   
    // Eğer template'den option'lar gelmemişse (fallback için)
    if (optionItems.length === 0) {
        console.warn("No options found from template, creating fallback options");
        
        // Bu durumda İngilizce fallback kullanın
        const helpChoices = [
            ['buy', 'I would like to buy Aminol products.'],
            ['become_dealer', 'I am interested in becoming a distributor.'],
            ['technical', 'I need technical support.'],
            ['other', 'Other']
        ];
       
        helpChoices.forEach(choice => {
            const option = document.createElement('div');
            option.className = 'custom-option';
            option.setAttribute('data-value', choice[0]);
            option.textContent = choice[1];
            customOptions.appendChild(option);
           
            option.addEventListener('click', function(e) {
                selectOption(this);
            });
        });
    } else {
        // Template'den gelen option'lara click event'i ekle
        optionItems.forEach(option => {
            option.addEventListener('click', function(e) {
                selectOption(this);
            });
        });
    }
   
    function selectOption(option) {
        const selectedText = option.textContent.trim();
        const selectedValue = option.getAttribute('data-value') || selectedText;
       
        customSelect.textContent = selectedText;
        hiddenInput.value = selectedValue;
       
        document.querySelectorAll('.custom-option').forEach(opt =>
            opt.classList.remove('selected'));
        option.classList.add('selected');
       
        customOptions.classList.remove('active');
        customSelect.classList.remove('open');
    }
   
    customSelect.addEventListener('click', function (e) {
        e.stopPropagation();
        this.classList.toggle('open');
        customOptions.classList.toggle('active');
    });
   
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('custom-option')) {
            e.stopPropagation();
            selectOption(e.target);
        }
    });
   
    document.addEventListener('click', function () {
        customOptions.classList.remove('active');
        customSelect.classList.remove('open');
    });
   
    // İlk option'ı default olarak seç (template'den gelen ilk seçenek)
    const firstOption = document.querySelector('.custom-option[data-value="buy"]') || 
                       document.querySelector('.custom-option');
    if (firstOption) {
        firstOption.classList.add('selected');
        // Custom select'in metnini de güncelle
        customSelect.textContent = firstOption.textContent.trim();
        hiddenInput.value = firstOption.getAttribute('data-value');
    }

    // reCAPTCHA validation functions
    function showRecaptchaError(message) {
        // Remove existing error message
        const existingError = document.querySelector('.recaptcha-error');
        if (existingError) {
            existingError.remove();
        }

        // Create new error message
        const recaptchaContainer = document.querySelector('.g-recaptcha');
        if (recaptchaContainer) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'recaptcha-error alert alert-danger';
            errorDiv.style.cssText = 'color: #d32f2f; font-size: 14px; margin-top: 5px; padding: 8px; background: #ffebee; border: 1px solid #ffcdd2; border-radius: 4px;';
            errorDiv.textContent = message;
            recaptchaContainer.parentNode.insertBefore(errorDiv, recaptchaContainer.nextSibling);
        }
    }

    function clearRecaptchaError() {
        const existingError = document.querySelector('.recaptcha-error');
        if (existingError) {
            existingError.remove();
        }
    }

    function validateRecaptcha() {
        const recaptchaResponse = grecaptcha.getResponse();
        
        if (!recaptchaResponse) {
            showRecaptchaError('Please complete the reCAPTCHA verification.');
            return false;
        }
        
        clearRecaptchaError();
        return true;
    }

    // Form submission handler with reCAPTCHA validation
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            // Check if reCAPTCHA is loaded
            if (typeof grecaptcha === 'undefined') {
                e.preventDefault();
                showRecaptchaError('reCAPTCHA failed to load. Please refresh the page and try again.');
                return false;
            }

            // Validate reCAPTCHA
            if (!validateRecaptcha()) {
                e.preventDefault();
                return false;
            }

            // Additional form validations can be added here
            const requiredFields = contactForm.querySelectorAll('[required]');
            let hasEmptyFields = false;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    hasEmptyFields = true;
                    field.style.borderColor = '#d32f2f';
                } else {
                    field.style.borderColor = '';
                }
            });

            if (hasEmptyFields) {
                e.preventDefault();
                showRecaptchaError('Please fill in all required fields.');
                return false;
            }

            // If all validations pass, show loading state
            const submitButton = contactForm.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = 'Sending... <i class="fa-solid fa-spinner fa-spin"></i>';
            }
        });
    }

    // reCAPTCHA callback functions (global scope)
    window.onRecaptchaSuccess = function() {
        clearRecaptchaError();
        console.log('reCAPTCHA verified successfully');
    };

    window.onRecaptchaExpired = function() {
        showRecaptchaError('reCAPTCHA has expired. Please verify again.');
        console.log('reCAPTCHA expired');
    };

    window.onRecaptchaError = function() {
        showRecaptchaError('reCAPTCHA verification failed. Please try again.');
        console.log('reCAPTCHA error occurred');
    };

    // Reset form state if needed
    window.resetContactForm = function() {
        if (contactForm) {
            const submitButton = contactForm.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.innerHTML = 'Send <i class="fa-solid fa-paper-plane"></i>';
            }
        }
        
        if (typeof grecaptcha !== 'undefined') { 
            grecaptcha.reset();
        }
        
        clearRecaptchaError();
    };

    // Handle form reset on page navigation back
    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            resetContactForm();
        }
    });
});