/**
 * Dynamic Game Progress Calculator
 * Calculates and updates the progress bar based on the current page in the game flow
 */

(function() {
    'use strict';

    // Define the game flow sequence
    // This should match the actual game flow order
    const GAME_FLOW = [
        'preview',              // 0% - First mission preview
        'ubung-1',              // ~5% - Safety anchor
        'ubung-2',              // ~10% - Team potential
        'ubung-3',              // ~15% - Fear
        'wartezimmer',          // ~20% - Waiting room
        'ubung-5',              // ~40% - Team tensions
        'ubung-4',              // ~65% - Safety score
        'psychologischer',      // ~80% - Safety result
        'spannungsfelder',      // ~85% - Tensions result
        'preview-2',            // ~90% - Second mission preview
        'mission-2-ubung-1',    // ~92% - Social sensitivity
        'mission-2-ubung-2',   // ~95% - Development feedbacks
        'assessment',           // ~98% - Game insights
        'arche'                 // 100% - Farewell
    ];

    /**
     * Get the current page identifier from the URL
     */
    function getCurrentPage() {
        const path = window.location.pathname;
        // Remove leading and trailing slashes
        const cleanPath = path.replace(/^\/|\/$/g, '');
        
        // Check if path matches any game flow page
        for (let page of GAME_FLOW) {
            if (cleanPath === page || cleanPath.startsWith(page + '/')) {
                return page;
            }
        }
        
        // Fallback: try to extract from path
        const parts = cleanPath.split('/');
        return parts[0] || 'preview';
    }

    /**
     * Calculate progress percentage based on current page
     */
    function calculateProgress() {
        const currentPage = getCurrentPage();
        const currentIndex = GAME_FLOW.indexOf(currentPage);
        
        if (currentIndex === -1) {
            // Page not in flow, return 0 or a default value
            return 0;
        }
        
        // Calculate progress: (current step / total steps) * 100
        // Add a small buffer to show progress within the current step
        const totalSteps = GAME_FLOW.length;
        const baseProgress = (currentIndex / totalSteps) * 100;
        
        // Add 50% of the step size to show we're in the middle of this step
        const stepSize = 100 / totalSteps;
        const progress = Math.min(100, baseProgress + (stepSize * 0.5));
        
        return Math.round(progress);
    }

    /**
     * Update the progress bar on the page
     */
    function updateProgressBar() {
        // Try multiple selectors to find the progress bar
        let progressBar = document.querySelector('#game-progress-bar');
        if (!progressBar) {
            progressBar = document.querySelector('.progress__bar > div');
        }
        if (!progressBar) {
            progressBar = document.querySelector('.progress__bar div');
        }
        
        if (!progressBar) {
            console.warn('GameProgress: Progress bar element not found');
            return;
        }
        
        const progress = calculateProgress();
        progressBar.style.width = progress + '%';
        
        // Update text content if it exists
        if (progressBar.textContent !== undefined) {
            progressBar.textContent = progress + '%';
        }
    }

    /**
     * Initialize progress bar on page load
     */
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', updateProgressBar);
        } else {
            updateProgressBar();
        }
        
        // Also update after a short delay to ensure all elements are rendered
        setTimeout(updateProgressBar, 100);
    }

    // Initialize when script loads
    init();

    // Export for potential external use
    if (typeof window !== 'undefined') {
        window.GameProgress = {
            calculate: calculateProgress,
            update: updateProgressBar,
            getCurrentPage: getCurrentPage
        };
    }
})();

