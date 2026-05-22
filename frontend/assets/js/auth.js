/**
 * Time Climb: Authentication Handlers
 * Manages Login and Signup form logic.
 */

import { apiClient } from './api.js';
import { updateState, saveState } from './state.js';

document.addEventListener('DOMContentLoaded', () => {
    initAuthForms();
});

function initAuthForms() {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
    }
}

/**
 * Handle User Login
 */
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');

    try {
        setLoading(submitBtn, true);

        const data = await apiClient('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });

        if (data && data.access_token) {
            // Update app state
            updateState('auth', {
                user: { id: data.user_id, email: email },
                token: data.access_token,
                isAuthenticated: true
            });
            
            saveState();
            
            // Redirect to dashboard
            window.location.href = 'dashboard.html';
        }
    } catch (error) {
        alert(`Login failed: ${error.message}`);
    } finally {
        setLoading(submitBtn, false);
    }
}

/**
 * Handle User Signup
 */
async function handleSignup(e) {
    e.preventDefault();
    const fullName = document.getElementById('full-name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');

    try {
        setLoading(submitBtn, true);

        const data = await apiClient('/auth/signup', {
            method: 'POST',
            body: JSON.stringify({ 
                full_name: fullName,
                email, 
                password 
            })
        });

        if (data) {
            alert('Account created successfully! Please sign in.');
            window.location.href = 'login.html';
        }
    } catch (error) {
        alert(`Signup failed: ${error.message}`);
    } finally {
        setLoading(submitBtn, false);
    }
}

/**
 * Helper to manage button loading state
 */
function setLoading(button, isLoading) {
    if (!button) return;
    
    if (isLoading) {
        button.disabled = true;
        button.dataset.originalText = button.textContent;
        button.textContent = 'Authenticating...';
    } else {
        button.disabled = false;
        button.textContent = button.dataset.originalText || button.textContent;
    }
}
