

document.addEventListener("DOMContentLoaded", function () {
  const tabs = document.querySelectorAll(".tab");
  const tabContents = document.querySelectorAll(".tab-content");

  function getResponsiveValues() {
    const screenWidth = window.innerWidth;

    if (screenWidth <= 400) {
      return { baseTop: 90, interval: 210 };
    }
    else if (screenWidth <= 370) {
      return { baseTop: 100, interval: 250 };
    }
    else if (screenWidth <= 422) {
      return { baseTop: 100, interval: 300 };
    }
    else if (screenWidth <= 439) {
      return { baseTop: 100, interval: 280 };
    }
    else if (screenWidth <= 440) {
      return { baseTop: 100, interval: 300 };
    }
    else if (screenWidth <= 480) {
      return { baseTop: 100, interval: 270 };
    }
    else if (screenWidth <= 540) {
      return { baseTop: 120, interval: 330 };
    }
    else if (screenWidth <= 630) {
      return { baseTop: 120, interval: 300 };
    }
    else if (screenWidth <= 670) {
      return { baseTop: 120, interval: 285 };
    }
    else if (screenWidth <= 768) {
      return { baseTop: 120, interval: 250 };
    } else if (screenWidth <= 1024) {
      return { baseTop: 130, interval: 320 };
    } else {
      return { baseTop: 140, interval: 360 };
    }
  }

  function positionDroplets(activeTabId) {
    const droplets = document.querySelectorAll(`#${activeTabId} .droplet`);
    const { baseTop, interval } = getResponsiveValues();

    droplets.forEach((droplet, index) => {
      const topPosition = baseTop + index * interval;
      droplet.style.top = `${topPosition}px`;
      console.log(`Droplet ${index + 1} in ${activeTabId}: ${topPosition}px`);
    });
  }

  function switchTab(tabId) {
    // Hide all tab contents
    tabContents.forEach((content) => {
      content.classList.remove("active");
    });

    tabs.forEach((tab) => {
      tab.classList.remove("active");
    });

    const selectedContent = document.getElementById(tabId);
    selectedContent.classList.add("active");

    document.querySelector(`[data-tab="${tabId}"]`).classList.add("active");

    positionDroplets(tabId);
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
    positionDroplets(activeTabId);
  }

  // Resize event əlavə edildi
  window.addEventListener('resize', function () {
    const activeTab = document.querySelector(".tab.active");
    if (activeTab) {
      const activeTabId = activeTab.getAttribute("data-tab");
      positionDroplets(activeTabId);
    }
  });
});