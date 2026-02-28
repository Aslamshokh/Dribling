// API Configuration
const CONFIG = {
    // Замените на URL вашего бэкенда когда он будет готов
    API_BASE_URL: 'https://your-backend-url.com/api',
    
    // Для разработки можно использовать локальный сервер
    // API_BASE_URL: 'http://localhost:8000/api',
    
    // Настройки приложения
    APP_NAME: 'Dribbling',
    DEFAULT_CITY: 'Пенджикент',
    DEFAULT_LAT: 39.4952,
    DEFAULT_LON: 67.6093
};

// Экспортируем для использования в других файлах
window.CONFIG = CONFIG;