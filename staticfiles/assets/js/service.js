document.addEventListener('DOMContentLoaded', function () {
    const customSelect = document.querySelector('.custom-select');
    const customOptions = document.querySelector('.custom-options');
    const optionItems = document.querySelectorAll('.custom-option');
    const hiddenInput = document.querySelector('#helpType');
   
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
});