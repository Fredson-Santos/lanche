// import api from './api'
import { salesService } from './salesService'

const delay = (ms = 400) => new Promise(r => setTimeout(r, ms))

export const reportService = {
  async getVendas({ inicio, fim } = {}) {
    await delay()
    return salesService.getAll({ inicio, fim })
    // return api.get('/api/relatorios/vendas', { params: { inicio, fim } })
  },

  async getFaturamento({ inicio, fim } = {}) {
    await delay()
    const resp = await salesService.getAll({ inicio, fim })
    const vendas = resp.data
    const total = vendas.reduce((acc, v) => acc + v.total, 0)
    return { data: { total, count: vendas.length } }
    // return api.get('/api/relatorios/faturamento', { params: { inicio, fim } })
  },

  async getVendasPorDia({ inicio, fim } = {}) {
    await delay()
    const resp = await salesService.getAll({ inicio, fim })
    const vendas = resp.data
    const grouped = {}
    vendas.forEach(v => {
      const day = v.data_venda.slice(0, 10)
      if (!grouped[day]) grouped[day] = { data: day, total: 0, count: 0 }
      grouped[day].total += v.total
      grouped[day].count += 1
    })
    return { data: Object.values(grouped).sort((a,b) => a.data.localeCompare(b.data)) }
  },
}
