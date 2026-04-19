import api from './api'

export const productService = {
  async getAll() {
    return api.get('/api/produtos/')
  },

  async getById(id) {
    return api.get(`/api/produtos/${id}`)
  },

  async create(data) {
    return api.post('/api/produtos/', data)
  },

  async update(id, data) {
    return api.put(`/api/produtos/${id}`, data)
  },

  async toggleAtivo(id) {
    return api.patch(`/api/produtos/${id}/toggle`)
  },

  async remove(id) {
    return api.delete(`/api/produtos/${id}`)
  },
}
