/**
 * AnyLaw API Client
 * Handles all communication with the backend API
 */

// Get API URL from environment or default to same origin
const API_BASE_URL = window.ENV?.API_URL || window.location.origin;

const api = {
    baseUrl: API_BASE_URL,

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
    },

    /**
     * Find case by citation
     */
    findByCitation: async (citation) => {
        const encoded = encodeURIComponent(citation);
        const response = await fetch(`${api.baseUrl}/api/citation/${encoded}`);
        if (!response.ok) throw new Error('Citation not found');
        return await response.json();
    },

    /**
     * Get all citations (with limit)
     */
    getCitations: async (limit = 100) => {
        const response = await fetch(`${api.baseUrl}/api/citations?limit=${limit}`);
        if (!response.ok) throw new Error('Failed to fetch citations');
        return await response.json();
    }
};

// Export to global scope
window.api = api;

console.log('AnyLaw API Client loaded. Backend:', API_BASE_URL);

