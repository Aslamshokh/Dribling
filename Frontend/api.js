class API {
    constructor(baseUrl) {
        this.baseUrl = baseUrl || window.CONFIG?.API_BASE_URL || 'https://your-backend-url.com/api';
    }

    async request(endpoint, options = {}) {
        const initData = window.Telegram?.WebApp?.initData;
        
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        // Добавляем Telegram данные если они есть
        if (initData) {
            headers['X-Telegram-Init-Data'] = initData;
        }

        try {
            console.log(`Making request to: ${this.baseUrl}${endpoint}`);
            
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                ...options,
                headers
            });

            if (!response.ok) {
                let errorMessage = 'API request failed';
                try {
                    const error = await response.json();
                    errorMessage = error.detail || error.message || errorMessage;
                } catch (e) {
                    // Если не удалось распарсить JSON
                }
                throw new Error(errorMessage);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Matches
    async getMatches(filters = {}) {
        const params = new URLSearchParams();
        Object.entries(filters).forEach(([key, value]) => {
            if (value) params.append(key, value);
        });
        const queryString = params.toString();
        const endpoint = queryString ? `/matches?${queryString}` : '/matches';
        return this.request(endpoint);
    }

    async getMatch(id) {
        return this.request(`/matches/${id}`);
    }

    async createMatch(matchData) {
        return this.request('/matches', {
            method: 'POST',
            body: JSON.stringify(matchData)
        });
    }

    async joinMatch(matchId, team = null) {
        return this.request(`/matches/${matchId}/join`, {
            method: 'POST',
            body: JSON.stringify({ team })
        });
    }

    async leaveMatch(matchId) {
        return this.request(`/matches/${matchId}/leave`, {
            method: 'POST'
        });
    }

    // Users
    async getCurrentUser() {
        try {
            return await this.request('/users/me');
        } catch (error) {
            // Возвращаем тестового пользователя для разработки
            console.warn('Using mock user data');
            return {
                id: 1,
                telegram_id: 123456789,
                first_name: 'Тестовый',
                username: 'test_user',
                photo_url: null,
                rating: 15,
                matches_played: 15,
                wins: 8,
                losses: 7
            };
        }
    }

    async getUser(id) {
        return this.request(`/users/${id}`);
    }

    async getUserMatches(userId, status = 'all') {
        return this.request(`/users/${userId}/matches?status=${status}`);
    }

    // Leaderboard
    async getLeaderboard(limit = 100, offset = 0) {
        try {
            return await this.request(`/leaderboard?limit=${limit}&offset=${offset}`);
        } catch (error) {
            // Мок данные для разработки
            console.warn('Using mock leaderboard data');
            return {
                leaderboard: [
                    { rank: 1, name: 'Алишер', wins: 25, win_rate: 83, rating: 45 },
                    { rank: 2, name: 'Рустам', wins: 22, win_rate: 79, rating: 42 },
                    { rank: 3, name: 'Фаррух', wins: 20, win_rate: 77, rating: 38 },
                    { rank: 4, name: 'Шахром', wins: 18, win_rate: 75, rating: 35 },
                    { rank: 5, name: 'Далер', wins: 17, win_rate: 74, rating: 32 },
                ],
                current_user: { name: 'Вы', matches: 15, rating: 28 },
                current_user_rank: 8
            };
        }
    }

    // Cities
    async getCities() {
        return this.request('/matches/cities/list');
    }
}

// Создаем глобальный экземпляр API
window.api = new API();