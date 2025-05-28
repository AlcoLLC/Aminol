// document.addEventListener('DOMContentLoaded', function() {
//     // Həm desktop həm də mobile button-lar üçün
//     const buttons = document.querySelectorAll('.lang-btn button, .mobile-lang-btn button');
//     const form = document.getElementById('language-form');
//     const langInput = document.getElementById('language-input');

//     buttons.forEach(button => {
//         button.addEventListener('click', function() {
//             const lang = this.getAttribute('data-lang');
//             langInput.value = lang;
//             form.submit();
//         });
//     });
// });

// document.addEventListener('DOMContentLoaded', function() {
//     const languageButtons = document.querySelectorAll('.btn-az, .btn-en');
//     const languageForm = document.getElementById('language-form');
//     const languageInput = document.getElementById('language-input');

//     languageButtons.forEach(button => {
//         button.addEventListener('click', function() {
//             const lang = this.getAttribute('data-lang');
//             languageInput.value = lang;
//             languageForm.submit();
//         });
//     });
// });