document.addEventListener("DOMContentLoaded", function () {
    const cancelBtn = document.querySelector(".page-header .cancel-button");
    const searchInput = document.querySelector(".search-input");

    cancelBtn.addEventListener("click", function () {
      searchInput.value = "";
      searchInput.focus();    
    });
});