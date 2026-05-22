/**
 * Time Climb: Shared Application Logic
 */

import { getState, resetState } from './state.js';

document.addEventListener('DOMContentLoaded', () => {
    // 1. Check Authentication (Route Guards)
    if (!checkAuth()) return;

    // 2. Initialize Navigation
    initNavigation();
    
    // 3. Initialize Theme/UI elements
    initUI();
    
    // 4. Render Icons
    renderIcons();

    // 5. Setup Logout Handler
    initLogout();
});

/**
 * Enforce route protection
 * Returns true if allowed to proceed, false if redirecting
 */
function checkAuth() {
    const state = getState();
    const path = window.location.pathname;
    const page = path.split("/").pop() || 'index.html';
    
    const publicPages = ['index.html', 'login.html', 'signup.html', ''];
    const isPublicPage = publicPages.includes(page);

    // If logged in and on a public page (except index if we want them to see landing), 
    // maybe redirect to dashboard? Let's stay simple for now.
    if (state.auth.isAuthenticated && (page === 'login.html' || page === 'signup.html')) {
        window.location.href = 'dashboard.html';
        return false;
    }

    // If NOT logged in and on a private page, redirect to landing or login
    if (!state.auth.isAuthenticated && !isPublicPage) {
        window.location.href = 'login.html';
        return false;
    }

    return true;
}

/**
 * Initialize Logout button
 */
function initLogout() {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (confirm('Are you sure you want to end your climb?')) {
                resetState();
                window.location.href = 'index.html';
            }
        });
    }
}


/**
 * Handle sidebar toggles and active states
 */
function initNavigation() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebar-toggle');
    
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
        });
    }

    // Set active link based on current path
    const path = window.location.pathname;
    const page = path.split("/").pop() || 'index.html';
    
    document.querySelectorAll('.nav-item').forEach(link => {
        if (link.getAttribute('href') === page) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * Shared UI interactions (dropdowns, modals)
 */
function initUI() {
    // Placeholder for global interactions
}

/**
 * Micro-utility to render SVG path icons
 * Usage: <span class="icon" data-icon="dashboard"></span>
 */
const ICON_PATHS = {
    dashboard: "M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z",
    analytics: "M18 20V10M12 20V4M6 20v-6",
    planner: "M19 4H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zM16 2v4M8 2v4M3 10h18",
    upload: "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12",
    coach: "M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z",
    settings: "M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2zM12 15a3 3 0 1 1 0-6 3 3 0 0 1 0 6z",
    logout: "M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9",
    plus: "M12 5v14M5 12h14",
    user: "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 7a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
    bell: "M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 0 1-3.46 0",
    search: "M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM21 21l-4.35-4.35",
    check: "M20 6L9 17l-5-5",
    clock: "M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10zM12 6v6l4 2"
};

function renderIcons() {
    document.querySelectorAll('[data-icon]').forEach(el => {
        const iconName = el.getAttribute('data-icon');
        const path = ICON_PATHS[iconName];
        if (path) {
            el.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="${path}"></path>
                </svg>
            `;
        }
    });
}
