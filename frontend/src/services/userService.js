// import api from './api'

let MOCK_USERS = [
  { id: 1, username: 'Admin',       email: 'admin@lanche.com',   role: 'admin',   ativo: true,  data_criacao: '2026-01-01' },
  { id: 2, username: 'Gerente',     email: 'gerente@lanche.com', role: 'gerente', ativo: true,  data_criacao: '2026-01-02' },
  { id: 3, username: 'Caixa',       email: 'caixa@lanche.com',   role: 'caixa',   ativo: true,  data_criacao: '2026-01-05' },
  { id: 4, username: 'João Silva',  email: 'joao@lanche.com',    role: 'caixa',   ativo: true,  data_criacao: '2026-02-10' },
  { id: 5, username: 'Maria Costa', email: 'maria@lanche.com',   role: 'gerente', ativo: false, data_criacao: '2026-02-15' },
]

let _nextId = 6
const delay = (ms = 300) => new Promise(r => setTimeout(r, ms))

export const userService = {
  async getAll() {
    await delay()
    return { data: [...MOCK_USERS] }
    // return api.get('/api/usuarios')
  },

  async create(data) {
    await delay(500)
    const novo = {
      ...data,
      id: _nextId++,
      ativo: true,
      data_criacao: new Date().toISOString().slice(0, 10),
    }
    MOCK_USERS.push(novo)
    return { data: { ...novo } }
    // return api.post('/api/usuarios', data)
  },

  async update(id, data) {
    await delay(400)
    MOCK_USERS = MOCK_USERS.map(u => u.id === id ? { ...u, ...data } : u)
    const updated = MOCK_USERS.find(u => u.id === id)
    return { data: { ...updated } }
    // return api.put(`/api/usuarios/${id}`, data)
  },

  async toggleAtivo(id) {
    await delay(300)
    MOCK_USERS = MOCK_USERS.map(u => u.id === id ? { ...u, ativo: !u.ativo } : u)
    return { data: MOCK_USERS.find(u => u.id === id) }
  },

  async remove(id) {
    await delay(400)
    MOCK_USERS = MOCK_USERS.filter(u => u.id !== id)
    return { data: { ok: true } }
    // return api.delete(`/api/usuarios/${id}`)
  },
}
