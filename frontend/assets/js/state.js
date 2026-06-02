

export const appState = {
    auth: {
        user: null,
        token: null,
        isAuthenticated: false
    },

    tasks: [],

    analytics: {
        weeklyHours: [],
        productivityScore: 0,
        streak: 0
    },

    timetable: [],

    grades: [],

    weakSubjects: [],

    upcomingExams: [],

    coach: {
        conversations: []
    },

    settings: {
        theme: 'dark',
        studyHoursPerDay: 4,
        notifications: true
    }
};

const STORAGE_KEY = 'timeclimb_state';

/**
 * Helper to check if a JWT token is expired
 */
function isTokenExpired(token) {
    if (!token) return true;
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => 
            '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
        ).join(''));
        const payload = JSON.parse(jsonPayload);
        return payload.exp * 1000 < Date.now();
    } catch (e) {
        return true;
    }
}

/**
 * Deep merge source object into target object recursively
 */
function deepMerge(target, source) {
    for (const key in source) {
        if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
            if (!target[key]) target[key] = {};
            deepMerge(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
}

/**
 * Load saved state from localStorage
 */
export function loadState() {
    try {
        const savedState = localStorage.getItem(STORAGE_KEY);

        if (!savedState) return;

        const parsedState = JSON.parse(savedState);

        // Merge saved state into appState using deep merge
        deepMerge(appState, parsedState);

        // Validate token expiry if authenticated
        if (appState.auth.token && isTokenExpired(appState.auth.token)) {
            console.warn('Persisted session token has expired. Resetting state.');
            resetState();
        } else {
            console.log('State loaded successfully');
        }
    } catch (error) {
        console.error('Failed to load state:', error);
    }
}


/**
 * Save entire state to localStorage
 */
export function saveState() {
    try {
        localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify(appState)
        );
    } catch (error) {
        console.error('Failed to save state:', error);
    }
}

/**
 * Update a top-level state key
 * Example:
 * updateState('tasks', newTasks)
 */
export function updateState(key, value) {
    if (!(key in appState)) {
        console.warn(`State key "${key}" does not exist.`);
        return;
    }

    appState[key] = value;

    saveState();
}

/**
 * Update nested state safely
 * Example:
 * updateNestedState('settings', 'theme', 'light')
 */
export function updateNestedState(parentKey, childKey, value) {
    if (!(parentKey in appState)) {
        console.warn(`Parent state key "${parentKey}" does not exist.`);
        return;
    }

    if (typeof appState[parentKey] !== 'object') {
        console.warn(`"${parentKey}" is not an object.`);
        return;
    }

    appState[parentKey][childKey] = value;

    saveState();
}

/**
 * Reset application state
 * Useful for logout
 */
export function resetState() {
    localStorage.removeItem(STORAGE_KEY);

    appState.auth = {
        user: null,
        token: null,
        isAuthenticated: false
    };

    appState.tasks = [];

    appState.analytics = {
        weeklyHours: [],
        productivityScore: 0,
        streak: 0
    };

    appState.timetable = [];

    appState.grades = [];

    appState.weakSubjects = [];

    appState.upcomingExams = [];

    appState.coach = {
        conversations: []
    };

    appState.settings = {
        theme: 'dark',
        studyHoursPerDay: 4,
        notifications: true
    };

    console.log('State reset successfully');
}

/**
 * Get current app state
 */
export function getState() {
    return appState;
}

// Auto-load state on import
loadState();