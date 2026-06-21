// Override Furo's 3-click theme toggle with a 2-click light/dark cycle
(function() {
    'use strict';

    function initCustomThemeToggle() {
        function setTheme(mode) {
            if (mode !== "light" && mode !== "dark") {
                mode = "light";
            }
            document.body.dataset.theme = mode;
            localStorage.setItem("theme", mode);
            updateThemeIcons(mode);
        }

        function updateThemeIcons(currentTheme) {
            document.querySelectorAll('.theme-toggle-container').forEach(function(container) {
                container.querySelectorAll('[class*="theme-icon-when-"]').forEach(function(icon) {
                    icon.style.display = 'none';
                });
                var selector = currentTheme === 'light'
                    ? '.theme-icon-when-light'
                    : '.theme-icon-when-dark';
                var targetIcon = container.querySelector(selector);
                if (targetIcon) {
                    targetIcon.style.display = 'block';
                }
            });
        }

        function cycleTheme() {
            var currentTheme = localStorage.getItem("theme") || "light";
            setTheme(currentTheme === "light" ? "dark" : "light");
        }

        // Clone toggles to remove Furo's event listeners, attach ours
        document.querySelectorAll('.theme-toggle').forEach(function(toggle) {
            var newToggle = toggle.cloneNode(true);
            toggle.parentNode.replaceChild(newToggle, toggle);
            newToggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                cycleTheme();
            });
        });

        setTheme(localStorage.getItem("theme") || "light");
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(initCustomThemeToggle, 100);
        });
    } else {
        setTimeout(initCustomThemeToggle, 100);
    }
})();
