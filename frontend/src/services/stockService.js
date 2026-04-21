import api from './api'

export const stockService = {
  async getAll() {
    return api.get('/api/estoque/')
  },

  async getByProduto(produto_id) {
    return api.get(`/api/estoque/produto/${produto_id}`)
  },

  async update(id, quantidade, temperatura_atual = null) {
    return api.put(`/api/estoque/${id}`, { quantidade, temperatura_atual })
  },
}
