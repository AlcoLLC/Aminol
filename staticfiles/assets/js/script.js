document.addEventListener('DOMContentLoaded', function () {
    // Dropdown background functionality
    const dropdowns = document.querySelectorAll('.dropdown');
    const dropdownBackground = document.querySelector('.dropdown-background');

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('mouseenter', function () {
            dropdownBackground.style.display = 'block';
            dropdownBackground.style.visibility = 'visible';
            dropdownBackground.style.opacity = '1';
        });

        dropdown.addEventListener('mouseleave', function (e) {
            const relatedTarget = e.relatedTarget;
            if (!dropdown.contains(relatedTarget) && relatedTarget !== dropdownBackground && !dropdownBackground.contains(relatedTarget)) {
                hideDropdownBackground();
            }
        });
    });

    dropdownBackground.addEventListener('mouseleave', function (e) {
        const relatedTarget = e.relatedTarget;
        let isInDropdown = false;

        dropdowns.forEach(dropdown => {
            if (dropdown.contains(relatedTarget)) {
                isInDropdown = true;
            }
        });

        if (!isInDropdown) {
            hideDropdownBackground();
        }
    });

    function hideDropdownBackground() {
        dropdownBackground.style.visibility = 'hidden';
        dropdownBackground.style.opacity = '0';
        setTimeout(() => {
            if (dropdownBackground.style.opacity === '0') {
                dropdownBackground.style.display = 'none';
            }
        }, 100);
    }

    function setActiveLinks() {
        const currentPath = window.location.pathname;
        const allNavLinks = document.querySelectorAll('.navbar a[href]');
        
        allNavLinks.forEach(link => {
            link.classList.remove('active');
        });

        const dropdownParents = document.querySelectorAll('.dropdown > a');
        dropdownParents.forEach(parent => {
            parent.classList.remove('active');
        });

        const dropdownLinks = document.querySelectorAll('.dropdown-content a[href]');
        let activeDropdownFound = false;

        dropdownLinks.forEach(dropdownLink => {
            const linkPath = dropdownLink.getAttribute('href');
            
            if (linkPath === currentPath || (linkPath && linkPath !== '/' && currentPath.startsWith(linkPath))) {

                dropdownLink.classList.add('active');
                
                const parentDropdown = dropdownLink.closest('.dropdown');
                if (parentDropdown) {
                    const parentLink = parentDropdown.querySelector('> a');
                    if (parentLink) {
                        parentLink.classList.add('active');
                        activeDropdownFound = true;
                    }
                }
            }
        });


        if (!activeDropdownFound) {
            const regularNavLinks = document.querySelectorAll('.navbar a[href]:not(.dropdown-content a)');
            
            regularNavLinks.forEach(link => {
                const linkPath = link.getAttribute('href');

                if (linkPath === currentPath) {
                    link.classList.add('active');
                }

                else if (linkPath && linkPath !== '/' && linkPath !== '' && currentPath.startsWith(linkPath)) {
                    link.classList.add('active');
                }
            });
        }

        handleSpecialDropdownCases(currentPath);
    }

    function handleSpecialDropdownCases(currentPath) {
        const marketsPaths = ['/markets_automotive', '/markets_industrial', '/markets_shipping'];
        
        if (marketsPaths.includes(currentPath)) {
            const marketsDropdown = Array.from(document.querySelectorAll('.dropdown > a'))
                .find(link => link.textContent.trim().startsWith('Markets'));
            
            if (marketsDropdown) {
                marketsDropdown.classList.add('active');
            }

            const activeDropdownLink = document.querySelector(`.dropdown-content a[href="${currentPath}"]`);
            if (activeDropdownLink) {
                activeDropdownLink.classList.add('active');
            }
        }
        const servicesPaths = ['/service_aminol_dealer', '/service_laboratory', '/service_logistics'];
        
        if (servicesPaths.includes(currentPath)) {
            const servicesDropdown = Array.from(document.querySelectorAll('.dropdown > a'))
                .find(link => link.textContent.trim().startsWith('Services'));
            
            if (servicesDropdown) {
                servicesDropdown.classList.add('active');
            }
            const activeDropdownLink = document.querySelector(`.dropdown-content a[href="${currentPath}"]`);
            if (activeDropdownLink) {
                activeDropdownLink.classList.add('active');
            }
        }
    }

    setActiveLinks();

    window.addEventListener('popstate', setActiveLinks);
    window.updateActiveLinks = setActiveLinks;
    console.log('Active links set for path:', window.location.pathname);
});