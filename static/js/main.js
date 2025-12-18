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

// API client
const api = {
    baseUrl: window.location.origin,

    /**
     * Fetch statistics
     */
    getStats: async () => {
        const response = await fetch(`${api.baseUrl}/api/stats`);
        if (!response.ok) throw new Error('Failed to fetch stats');
        return await response.json();
    },

    /**
     * Search cases
     */
    search: async (query, filters = {}) => {
        const params = new URLSearchParams({
            q: query || '',
            limit: filters.limit || 20,
            offset: filters.offset || 0
        });

        if (filters.jurisdiction) params.append('jurisdiction', filters.jurisdiction);
        if (filters.year) params.append('year', filters.year);

        const response = await fetch(`${api.baseUrl}/api/search?${params}`);
        if (!response.ok) throw new Error('Failed to search');
        return await response.json();
    },

    /**
     * Get document by ID
     */
    getDocument: async (docId) => {
        const response = await fetch(`${api.baseUrl}/api/document/${docId}`);
        if (!response.ok) throw new Error('Document not found');
        return await response.json();
    },

    /**
     * Get jurisdictions list
     */
    getJurisdictions: async () => {
        const response = await fetch(`${api.baseUrl}/api/jurisdictions`);
        if (!response.ok) throw new Error('Failed to fetch jurisdictions');
        return await response.json();
    }
};

// Export to global scope
window.utils = utils;
window.api = api;

console.log('AnyLaw Database Navigator loaded');

