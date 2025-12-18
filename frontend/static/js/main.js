/**
 * AnyLaw Case Database Navigator
 * Main JavaScript utilities
 */

// Utility functions
const utils = {
    /**
     * Format a date string to a readable format
     */
    formatDate: (dateStr) => {
        if (!dateStr) return 'Unknown';
        try {
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        } catch {
            return dateStr;
        }
    },

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml: (text) => {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * Format large numbers with commas
     */
    formatNumber: (num) => {
        return num.toLocaleString('en-US');
    },

    /**
     * Estimate word count from byte length
     */
    estimateWords: (bytes) => {
        return Math.round(bytes / 5);
    },

    /**
     * Format bytes to KB/MB
     */
    formatBytes: (bytes) => {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    },

    /**
     * Debounce function for search
     */
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Export utils to global scope
window.utils = utils;

console.log('AnyLaw Utils loaded');

