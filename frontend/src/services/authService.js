import api from './api'

export const authService = {
  async login(email, senha) {
    const response = await api.post('/api/auth/login', { email, senha })
    // The backend returns TokenResponse which contains access_token and usuario
    return {
      access_token: response.data.access_token,
      user: response.data.usuario,
    }
  },

  async logout() {
    // Optionally call backend if a logout endpoint is implemented
    // await api.post('/api/auth/logout')
  },
}
