// import api from './api'
import { stockService } from './stockService'

const now = new Date()
const d = (daysAgo) => {
  const dt = new Date(now)
  dt.setDate(dt.getDate() - daysAgo)
  return dt.toISOString()
}

let MOCK_SALES = [
  { id: 1, usuario_id: 3, usuario_nome: 'Caixa',   total: 46.50, data_venda: d(0),  itens: [{ produto_id:1, nome:'X-Burguer', quantidade:2, preco_unitario:18.50, subtotal:37.00 }, { produto_id:7, nome:'Refrigerante', quantidade:1, preco_unitario:6.00, subtotal:6.00 }, { produto_id:5, nome:'Batata P.', quantidade:1, preco_unitario:8.00, subtotal:8.00 }] },
  { id: 2, usuario_id: 3, usuario_nome: 'Caixa',   total: 28.00, data_venda: d(0),  itens: [{ produto_id:2, nome:'X-Bacon',  quantidade:1, preco_unitario:22.00, subtotal:22.00 }, { produto_id:7, nome:'Refrigerante', quantidade:1, preco_unitario:6.00, subtotal:6.00 }] },
  { id: 3, usuario_id: 2, usuario_nome: 'Gerente', total: 52.00, data_venda: d(1),  itens: [{ produto_id:9, nome:'Milk shake', quantidade:2, preco_unitario:16.00, subtotal:32.00 }, { produto_id:4, nome:'Hot Dog', quantidade:1, preco_unitario:12.00, subtotal:12.00 }, { produto_id:5, nome:'Batata P.', quantidade:1, preco_unitario:8.00, subtotal:8.00 }] },
  { id: 4, usuario_id: 3, usuario_nome: 'Caixa',   total: 37.00, data_venda: d(1),  itens: [{ produto_id:3, nome:'X-Salada', quantidade:2, preco_unitario:19.00, subtotal:38.00 }] },
  { id: 5, usuario_id: 3, usuario_nome: 'Caixa',   total: 63.00, data_venda: d(2),  itens: [{ produto_id:1, nome:'X-Burguer', quantidade:2, preco_unitario:18.50, subtotal:37.00 }, { produto_id:6, nome:'Batata G.', quantidade:2, preco_unitario:14.00, subtotal:28.00 }] },
  { id: 6, usuario_id: 2, usuario_nome: 'Gerente', total: 41.00, data_venda: d(3),  itens: [{ produto_id:2, nome:'X-Bacon', quantidade:1, preco_unitario:22.00, subtotal:22.00 }, { produto_id:8, nome:'Suco Natural', quantidade:1, preco_unitario:9.00, subtotal:9.00 }, { produto_id:4, nome:'Hot Dog', quantidade:1, preco_unitario:12.00, subtotal:12.00 }] },
  { id: 7, usuario_id: 3, usuario_nome: 'Caixa',   total: 55.00, data_venda: d(5),  itens: [{ produto_id:9, nome:'Milk shake', quantidade:1, preco_unitario:16.00, subtotal:16.00 }, { produto_id:2, nome:'X-Bacon', quantidade:1, preco_unitario:22.00, subtotal:22.00 }, { produto_id:6, nome:'Batata G.', quantidade:1, preco_unitario:14.00, subtotal:14.00 }] },
  { id: 8, usuario_id: 3, usuario_nome: 'Caixa',   total: 24.00, data_venda: d(7),  itens: [{ produto_id:4, nome:'Hot Dog', quantidade:2, preco_unitario:12.00, subtotal:24.00 }] },
]

let _nextSaleId = 9

const delay = (ms = 300) => new Promise(r => setTimeout(r, ms))

export const salesService = {
  async getAll({ inicio, fim } = {}) {
    await delay()
    let sales = [...MOCK_SALES]
    if (inicio) sales = sales.filter(s => new Date(s.data_venda) >= new Date(inicio))
    if (fim)    sales = sales.filter(s => new Date(s.data_venda) <= new Date(fim + 'T23:59:59'))
    return { data: sales.sort((a, b) => new Date(b.data_venda) - new Date(a.data_venda)) }
  },

  async getById(id) {
    await delay()
    const s = MOCK_SALES.find(s => s.id === id)
    if (!s) throw new Error('Venda não encontrada')
    return { data: { ...s } }
  },

  async create(itens, usuarioId, usuarioNome) {
    await delay(600)
    const total = itens.reduce((acc, i) => acc + i.subtotal, 0)
    const venda = {
      id: _nextSaleId++,
      usuario_id: usuarioId,
      usuario_nome: usuarioNome,
      total,
      data_venda: new Date().toISOString(),
      itens,
    }
    MOCK_SALES.unshift(venda)
    // Subtract stock
    for (const item of itens) {
      await stockService.subtract(item.produto_id, item.quantidade)
    }
    return { data: { ...venda } }
    // return api.post('/api/vendas', { itens })
  },

  async getToday() {
    await delay()
    const today = new Date().toISOString().slice(0, 10)
    const todaySales = MOCK_SALES.filter(s => s.data_venda.slice(0, 10) === today)
    const total = todaySales.reduce((acc, s) => acc + s.total, 0)
    return { data: { count: todaySales.length, total } }
  },
}
