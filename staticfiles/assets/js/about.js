document.addEventListener("DOMContentLoaded", function () {
  const tabs = document.querySelectorAll(".tab");
  const tabContents = document.querySelectorAll(".tab-content");

  function positionDroplets(activeTabId) {
    const droplets = document.querySelectorAll(`#${activeTabId} .droplet`);
    const baseTop = 140;
    const interval = 360;

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
});
