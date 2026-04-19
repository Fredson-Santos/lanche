// import api from './api'

let MOCK_STOCK = [
  { id: 1, produto_id: 1, nome: 'X-Burguer',      quantidade: 45 },
  { id: 2, produto_id: 2, nome: 'X-Bacon',         quantidade: 30 },
  { id: 3, produto_id: 3, nome: 'X-Salada',        quantidade: 25 },
  { id: 4, produto_id: 4, nome: 'Hot Dog',          quantidade: 8  },
  { id: 5, produto_id: 5, nome: 'Batata Pequena',   quantidade: 60 },
  { id: 6, produto_id: 6, nome: 'Batata Grande',    quantidade: 40 },
  { id: 7, produto_id: 7, nome: 'Refrigerante',     quantidade: 3  },
  { id: 8, produto_id: 8, nome: 'Suco Natural',     quantidade: 20 },
  { id: 9, produto_id: 9, nome: 'Milk shake',       quantidade: 15 },
  { id:10, produto_id:10, nome: 'Onion Rings',      quantidade: 0  },
]

const delay = (ms = 300) => new Promise(r => setTimeout(r, ms))

export const stockService = {
  async getAll() {
    await delay()
    return { data: [...MOCK_STOCK] }
    // return api.get('/api/estoque')
  },

  async getByProduto(produto_id) {
    await delay()
    const item = MOCK_STOCK.find(s => s.produto_id === produto_id)
    return { data: item ? { ...item } : null }
  },

  async update(id, quantidade) {
    await delay(400)
    MOCK_STOCK = MOCK_STOCK.map(s => s.id === id ? { ...s, quantidade } : s)
    const updated = MOCK_STOCK.find(s => s.id === id)
    return { data: { ...updated } }
    // return api.put(`/api/estoque/${id}`, { quantidade })
  },

  // Called internally after a sale
  async subtract(produto_id, qtd) {
    await delay(200)
    MOCK_STOCK = MOCK_STOCK.map(s =>
      s.produto_id === produto_id
        ? { ...s, quantidade: Math.max(0, s.quantidade - qtd) }
        : s
    )
  },
}
