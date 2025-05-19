document.addEventListener('DOMContentLoaded', function () {
    const customSelect = document.querySelector('.custom-select');
    const customOptions = document.querySelector('.custom-options');
    const optionItems = document.querySelectorAll('.custom-option');
    const hiddenInput = document.querySelector('#helpType');

    customSelect.addEventListener('click', function (e) {
        e.stopPropagation();
        customSelect.classList.toggle('open');
        customOptions.classList.toggle('active');
    });

    optionItems.forEach(option => {
        option.addEventListener('click', function (e) {
            e.stopPropagation();

            const selectedText = this.textContent.trim();
            const selectedValue = this.getAttribute('data-value') || selectedText;

            customSelect.textContent = selectedText;
            hiddenInput.value = selectedValue;

            optionItems.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');

            customOptions.classList.remove('active');
            customSelect.classList.remove('open');
        });
    });

    document.addEventListener('click', function () {
        customOptions.classList.remove('active');
        customSelect.classList.remove('open');
    });
});