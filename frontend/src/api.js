import axios from 'axios';

// Production API URL - hardcoded for deployment
const API_URL = 'https://hrms-lite-api-lrfv.onrender.com/api';

// Export for use in components
export const API_BASE_URL = API_URL;

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Log errors for debugging
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.message);
    return Promise.reject(error);
  }
);
