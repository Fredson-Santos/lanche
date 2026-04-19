import api from './api'

export const salesService = {
  async getAll({ inicio, fim } = {}) {
    return api.get('/api/vendas/', { params: { inicio, fim } })
  },

  async getById(id) {
    return api.get(`/api/vendas/${id}`)
  },

  async create(itens, usuarioId, usuarioNome) {
    // Backend VendaCreate expects only:
    // usuario_id: int
    // itens: list[ItemVendaCreate] -> [{ produto_id: int, quantidade: int, preco_unitario: float }]
    const payload = {
      usuario_id: usuarioId,
      itens: itens.map(i => ({ 
        produto_id: i.produto_id, 
        quantidade: i.quantidade,
        preco_unitario: i.preco_unitario
      }))
    }
    return api.post('/api/vendas/', payload)
  },

  async getToday() {
    // We can rely on reportService or just pass today's date
    const today = new Date().toISOString().slice(0, 10)
    const resp = await api.get('/api/vendas/', { params: { inicio: today, fim: today } })
    const vendas = resp.data || []
    const total = vendas.reduce((acc, s) => acc + s.total, 0)
    return { data: { count: vendas.length, total } }
  },
}
