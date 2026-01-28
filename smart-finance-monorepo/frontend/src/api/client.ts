import axios from 'axios';

// 1. Create a base client
const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000', // Our Python Backend
    headers: {
        'Content-Type': 'application/json',
    },
});

// 2. NEW: AI Client (Port 8001)
const aiClient = axios.create({
    baseURL: 'http://127.0.0.1:8001',
    headers: { 'Content-Type': 'application/json' },
});

// 2. Define the types (matching our Python Pydantic models)
export interface Transaction {
    id?: string;
    user_id: string;
    amount: number;
    description: string;
    date: string; // ISO Date string (YYYY-MM-DD)
    type: 'income' | 'expense';
    category_id?: number;
}

// 3. API Functions
export const api = {
    // Create a new user (for testing)
    createUser: async (email: string) => {
        const response = await apiClient.post('/users/', { email });
        return response.data;
    },

    // Add a transaction
    addTransaction: async (data: Transaction) => {
        // We pass the user_id as a query param or inside body depending on your backend setup.
        // Based on our Phase 2 code: user_id is a query param.
        const response = await apiClient.post(`/transactions/?user_id=${data.user_id}`, data);
        return response.data;
    },

    // Get transactions
    getTransactions: async (userId: string) => {
        const response = await apiClient.get(`/transactions/${userId}`);
        return response.data;
    },
    getAdvice: async (userId: string) => {
        // We hit the AI microservice here
        const response = await aiClient.post('/analyze', { user_id: userId });
        return response.data.advice;
    }
};