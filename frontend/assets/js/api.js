/**
 * Time Climb: Centralized API Client
 * Handles base URL, auth headers, and global error handling.
 */

import { getState, resetState } from './state.js';

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Enhanced fetch wrapper
 * @param {string} endpoint - API endpoint (e.g., '/auth/login')
 * @param {object} options - Fetch options
 */
export async function apiClient(endpoint, options = {}) {
    const state = getState();
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Setup default headers
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    // Automatically inject Bearer token if available
    if (state.auth.token) {
        headers['Authorization'] = `Bearer ${state.auth.token}`;
    }

    const config = {
        ...options,
        headers
    };

    try {
        const response = await fetch(url, config);
        
        // Handle global 401 Unauthorized (invalid/expired token)
        if (response.status === 401) {
            console.warn('Unauthorized request. Redirecting to login...');
            resetState();
            
            // Avoid redirect loops if already on login/signup/index
            const publicPages = ['index.html', 'login.html', 'signup.html'];
            const currentPage = window.location.pathname.split('/').pop() || 'index.html';
            
            if (!publicPages.includes(currentPage)) {
                window.location.href = 'login.html';
            }
            return null;
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'API request failed');
        }

        return data;
    } catch (error) {
        console.error(`API Error [${endpoint}]:`, error);
        throw error;
    }
}
