import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  register: (email: string, password: string, full_name?: string) =>
    api.post('/auth/register', { email, password, full_name }),
  getMe: () => api.get('/auth/me'),
};

// Agent APIs
export const agentAPI = {
  getTemplates: () => api.get('/agents/templates'),
  create: (data: any) => api.post('/agents', data),
  list: () => api.get('/agents'),
  get: (id: string) => api.get(`/agents/${id}`),
  delete: (id: string) => api.delete(`/agents/${id}`),
};

// Task APIs
export const taskAPI = {
  create: (data: any) => api.post('/tasks', data),
  list: () => api.get('/tasks'),
  get: (id: string) => api.get(`/tasks/${id}`),
  execute: (id: string) => api.post(`/tasks/${id}/execute`),
};
