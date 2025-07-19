// Custom 2-click theme toggle - Override Furo's default 3-click behavior
(function() {
    'use strict';
    
    // Wait for DOM and ensure we override after Furo loads
    function initCustomThemeToggle() {
        // Custom theme setting function
        function setTheme(mode) {
            if (mode !== "light" && mode !== "dark") {
                mode = "light"; // Default to light if invalid
            }
            
            document.body.dataset.theme = mode;
            localStorage.setItem("theme", mode);
            
            // Update all theme icons to reflect current state
            updateThemeIcons(mode);
        }
        
        // Update theme icon visibility based on current theme
        function updateThemeIcons(currentTheme) {
            const themeContainers = document.querySelectorAll('.theme-toggle-container');
            themeContainers.forEach(function(container) {
                const icons = container.querySelectorAll('[class*="theme-icon-when-"]');
                icons.forEach(function(icon) {
                    icon.style.display = 'none';
                });
                
                // Show appropriate icon based on current theme
                const targetIcon = container.querySelector(
                    currentTheme === 'light' ? 
                    '.theme-icon-when-light' : 
                    '.theme-icon-when-dark'
                );
                if (targetIcon) {
                    targetIcon.style.display = 'block';
                }
            });
        }
        
        // Simple 2-click cycle: light ↔ dark
        function cycleTheme() {
            const currentTheme = localStorage.getItem("theme") || "light";
            const newTheme = currentTheme === "light" ? "dark" : "light";
            setTheme(newTheme);
        }
        
        // Replace theme toggle event handlers
        function attachCustomHandlers() {
            const themeToggles = document.querySelectorAll('.theme-toggle');
            
            themeToggles.forEach(function(toggle) {
                // Remove existing event listeners
                const newToggle = toggle.cloneNode(true);
                toggle.parentNode.replaceChild(newToggle, toggle);
                
                // Add our custom click handler
                newToggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    cycleTheme();
                });
            });
        }
        
        // Initialize theme
        function initTheme() {
            const savedTheme = localStorage.getItem("theme");
            const initialTheme = savedTheme || "light";
            setTheme(initialTheme);
        }
        
        // Main initialization
        attachCustomHandlers();
        initTheme();
    }
    
    // Initialize when DOM is ready, with a small delay to ensure Furo is loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(initCustomThemeToggle, 100);
        });
    } else {
        setTimeout(initCustomThemeToggle, 100);
    }
})();