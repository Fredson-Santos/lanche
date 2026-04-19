import api from './api'

export const userService = {
  async getAll() {
    return api.get('/api/usuarios/')
  },

  async create(data) {
    return api.post('/api/usuarios/', data)
  },

  async update(id, data) {
    return api.put(`/api/usuarios/${id}`, data)
  },

  async toggleAtivo(id) {
    return api.patch(`/api/usuarios/${id}/toggle`)
  },

  async remove(id) {
    return api.delete(`/api/usuarios/${id}`)
  },
}
