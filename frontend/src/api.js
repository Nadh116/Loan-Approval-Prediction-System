import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const predictLoan = async (loanData) => {
    try {
        const response = await api.post('/predict', loanData);
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.error || 'Prediction failed');
    }
};

export const getModelInfo = async () => {
    try {
        const response = await api.get('/model-info');
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.error || 'Failed to get model info');
    }
};

export const checkHealth = async () => {
    try {
        const response = await api.get('/');
        return response.data;
    } catch (error) {
        throw new Error('Backend server is not running');
    }
};

export default api;