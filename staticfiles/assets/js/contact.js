// // Add this to your JavaScript file (or in a script tag at the bottom of your template)

// document.addEventListener('DOMContentLoaded', function() {
//     // For debugging
//     console.log('Help choices in template:', JSON.stringify(
//         Array.from(document.querySelectorAll('.custom-option')).map(el => ({
//             value: el.dataset.value,
//             text: el.textContent
//         }))
//     ));

//     const customSelect = document.querySelector('.custom-select');
//     const customOptions = document.querySelector('.custom-options');
//     const hiddenInput = document.getElementById('helpType');
//     const options = document.querySelectorAll('.custom-option');

//     // Toggle custom select dropdown
//     if (customSelect) {
//         customSelect.addEventListener('click', function() {
//             customOptions.classList.toggle('show');
//         });
//     }

//     // Handle option selection
//     options.forEach(option => {
//         option.addEventListener('click', function() {
//             const value = this.getAttribute('data-value');
//             const text = this.textContent;
            
//             // Update display
//             customSelect.textContent = text;
            
//             // Update hidden input value
//             hiddenInput.value = value;
            
//             // Hide options after selection
//             customOptions.classList.remove('show');
            
//             console.log('Selected:', value, text);
//         });
//     });

//     // Close dropdown when clicking outside
//     document.addEventListener('click', function(e) {
//         if (!e.target.closest('.custom-select-wrapper')) {
//             customOptions.classList.remove('show');
//         }
//     });
// });