document.addEventListener("DOMContentLoaded", function () {
  const tabs = document.querySelectorAll(".tab");
  const tabContents = document.querySelectorAll(".tab-content");

  function positionDropletsDynamically(container) {
    const sectionRows = container.querySelectorAll('.section-row');
    const droplets = container.querySelectorAll('.droplet');

    sectionRows.forEach((row, index) => {
      const droplet = droplets[index];
      if (droplet && row) {

        const rowRect = row.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();

        const relativeTop = rowRect.top - containerRect.top;
        const rowHeight = rowRect.height;
        
        const dropletPosition = relativeTop + (rowHeight / 2) - 15; 
        
        droplet.style.top = `${dropletPosition}px`;
        
        console.log(`Droplet ${index + 1}: Row top: ${relativeTop}px, Row height: ${rowHeight}px, Droplet position: ${dropletPosition}px`);
      }
    });
  }

  function positionDropletsForTab(activeTabId) {
    const activeTabContent = document.getElementById(activeTabId);
    if (activeTabContent) {
      const container = activeTabContent.querySelector('.shared-images-container');
      if (container) {
        setTimeout(() => {
          positionDropletsDynamically(container);
        }, 100);
      }
    }
  }

  function positionAllDropletsDynamically() {
    const containers = document.querySelectorAll('.shared-images-container');
    
    containers.forEach(container => {
      setTimeout(() => {
        positionDropletsDynamically(container);
      }, 100);
    });
  }

  if (tabs.length > 0) {
    function switchTab(tabId) {
      tabContents.forEach((content) => {
        content.classList.remove("active");
      });

      tabs.forEach((tab) => {
        tab.classList.remove("active");
      });

      const selectedContent = document.getElementById(tabId);
      selectedContent.classList.add("active");

      document.querySelector(`[data-tab="${tabId}"]`).classList.add("active");

      positionDropletsForTab(tabId);
    }

    tabs.forEach((tab) => {
      tab.addEventListener("click", function () {
        const tabId = this.getAttribute("data-tab");
        switchTab(tabId);
      });
    });

    const activeTab = document.querySelector(".tab.active");
    if (activeTab) {
      const activeTabId = activeTab.getAttribute("data-tab");
      positionDropletsForTab(activeTabId);
    }

    window.addEventListener('resize', function () {
      const activeTab = document.querySelector(".tab.active");
      if (activeTab) {
        const activeTabId = activeTab.getAttribute("data-tab");
        setTimeout(() => {
          positionDropletsForTab(activeTabId);
        }, 200);
      }
    });
  } 
  else {
    positionAllDropletsDynamically();

    window.addEventListener('resize', function () {
      setTimeout(() => {
        positionAllDropletsDynamically();
      }, 200);
    });
  }

  window.addEventListener('load', function() {
    if (tabs.length > 0) {
      const activeTab = document.querySelector(".tab.active");
      if (activeTab) {
        const activeTabId = activeTab.getAttribute("data-tab");
        setTimeout(() => {
          positionDropletsForTab(activeTabId);
        }, 300);
      }
    } else {
      setTimeout(() => {
        positionAllDropletsDynamically();
      }, 300);
    }
  });
});