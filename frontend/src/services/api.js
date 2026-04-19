import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
})

// Request interceptor — inject JWT
api.interceptors.request.use(config => {
  const token = localStorage.getItem('lanche_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor — handle 401
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('lanche_token')
      localStorage.removeItem('lanche_user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
