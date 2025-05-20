document.addEventListener('DOMContentLoaded', function () {
    // Debug to check what help_choices are available
    console.log("Help choices from Django:", document.querySelectorAll('.custom-option'));
    
    const customSelect = document.querySelector('.custom-select');
    const customOptions = document.querySelector('.custom-options');
    const optionItems = document.querySelectorAll('.custom-option');
    const hiddenInput = document.querySelector('#helpType');
    
    // Check if elements exist before adding event listeners
    if (!customSelect || !customOptions) {
        console.error("Custom select elements not found!");
        return;
    }
    
    // If there are no option items, create them from the server-side data
    if (optionItems.length === 0) {
        // This is a fallback if the Django template isn't rendering the options
        const helpChoices = [
            ['buy', 'I would like to buy Aminol products.'],
            ['become_dealer', 'I would like to become an Aminol dealer.'],
            ['technical', 'I have a technical question.'],
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
    }
    
    // Function to handle option selection
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
    
    // Toggle dropdown on select click
    customSelect.addEventListener('click', function (e) {
        e.stopPropagation();
        this.classList.toggle('open');
        customOptions.classList.toggle('active');
    });
    
    // Add click handlers to all option items (both initial and potentially added later)
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('custom-option')) {
            e.stopPropagation();
            selectOption(e.target);
        }
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function () {
        customOptions.classList.remove('active');
        customSelect.classList.remove('open');
    });
    
    // Set initial value
    const defaultOption = document.querySelector('.custom-option[data-value="buy"]');
    if (defaultOption) {
        defaultOption.classList.add('selected');
    }
});