import api from './api'

export const reportService = {
  async getVendas({ inicio, fim } = {}) {
    return api.get('/api/relatorios/vendas', { params: { inicio, fim } })
  },

  async getFaturamento({ inicio, fim } = {}) {
    return api.get('/api/relatorios/faturamento', { params: { inicio, fim } })
  },

  async getVendasPorDia({ inicio, fim } = {}) {
    return api.get('/api/relatorios/vendas-por-dia', { params: { inicio, fim } })
  },
}
