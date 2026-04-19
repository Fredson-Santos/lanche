// import api from './api'

// ─── Mock data (remove when backend routes are live) ──────────────────────────
const MOCK_USERS = {
  'admin@lanche.com':   { id: 1, username: 'Admin',   email: 'admin@lanche.com',   role: 'admin',   ativo: true },
  'gerente@lanche.com': { id: 2, username: 'Gerente', email: 'gerente@lanche.com', role: 'gerente', ativo: true },
  'caixa@lanche.com':   { id: 3, username: 'Caixa',   email: 'caixa@lanche.com',   role: 'caixa',   ativo: true },
}

const MOCK_PASSWORDS = {
  'admin@lanche.com':   'admin123',
  'gerente@lanche.com': 'gerente123',
  'caixa@lanche.com':   'caixa123',
}
// ──────────────────────────────────────────────────────────────────────────────

export const authService = {
  async login(email, senha) {
    // ── MOCK ──
    await new Promise(r => setTimeout(r, 600)) // simulate latency
    const user = MOCK_USERS[email]
    if (!user || MOCK_PASSWORDS[email] !== senha) {
      const err = new Error('Credenciais inválidas')
      err.response = { data: { detail: 'Email ou senha incorretos.' } }
      throw err
    }
    return {
      access_token: `mock-jwt-token-${user.role}-${Date.now()}`,
      user,
    }
    // ── REAL (uncomment when backend ready) ──
    // const response = await api.post('/api/auth/login', { email, senha })
    // return response.data
  },

  async logout() {
    // await api.post('/api/auth/logout')
  },
}
