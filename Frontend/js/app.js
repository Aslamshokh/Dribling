// Telegram WebApp initialization
let tg = window.Telegram?.WebApp;

if (tg) {
    tg.expand();
    tg.enableClosingConfirmation();
    tg.setHeaderColor('#0f0f0f');
    tg.setBackgroundColor('#0f0f0f');
}

// State management
let currentUser = null;

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
    // Initialize user
    await initUser();
});

// Initialize user from Telegram data
async function initUser() {
    try {
        if (window.api) {
            currentUser = await window.api.getCurrentUser();
        }
    } catch (error) {
        console.error('Error initializing user:', error);
    }
}

// Navigation
function navigateTo(path) {
    window.location.href = path;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Show error message
function showError(message) {
    if (tg) {
        tg.showAlert(message);
    } else {
        alert(message);
    }
}

// Show loading
function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading';
    loadingDiv.innerHTML = '<div class="loading-spinner"></div>';
    return loadingDiv;
}

// Get players count text
function getPlayersText(current, max) {
    return `${current || 0}/${max}`;
}

// Экспортируем функции для использования в HTML
window.navigateTo = navigateTo;
window.formatDate = formatDate;
window.showError = showError;