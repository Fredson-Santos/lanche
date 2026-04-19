// import api from './api'

let MOCK_PRODUCTS = [
  { id: 1, nome: 'X-Burguer',       descricao: 'Pão, carne, queijo',       preco: 18.50, ativo: true,  data_criacao: '2026-01-10' },
  { id: 2, nome: 'X-Bacon',         descricao: 'Pão, carne, bacon, queijo', preco: 22.00, ativo: true,  data_criacao: '2026-01-10' },
  { id: 3, nome: 'X-Salada',        descricao: 'Pão, carne, salada',        preco: 19.00, ativo: true,  data_criacao: '2026-01-11' },
  { id: 4, nome: 'Hot Dog',         descricao: 'Salsicha, pão, mostarda',   preco: 12.00, ativo: true,  data_criacao: '2026-01-12' },
  { id: 5, nome: 'Batata Pequena',  descricao: 'Porção 100g',               preco: 8.00,  ativo: true,  data_criacao: '2026-01-12' },
  { id: 6, nome: 'Batata Grande',   descricao: 'Porção 200g',               preco: 14.00, ativo: true,  data_criacao: '2026-01-12' },
  { id: 7, nome: 'Refrigerante',    descricao: 'Lata 350ml',                preco: 6.00,  ativo: true,  data_criacao: '2026-01-15' },
  { id: 8, nome: 'Suco Natural',    descricao: 'Copo 400ml',                preco: 9.00,  ativo: true,  data_criacao: '2026-01-16' },
  { id: 9, nome: 'Milk shake',      descricao: '500ml diversas opções',     preco: 16.00, ativo: true,  data_criacao: '2026-02-01' },
  { id:10, nome: 'Onion Rings',     descricao: 'Porção anéis de cebola',    preco: 11.00, ativo: false, data_criacao: '2026-02-05' },
]

let _nextId = 11

const delay = (ms = 300) => new Promise(r => setTimeout(r, ms))

export const productService = {
  async getAll() {
    await delay()
    return { data: [...MOCK_PRODUCTS] }
    // return api.get('/api/produtos')
  },

  async getById(id) {
    await delay()
    const p = MOCK_PRODUCTS.find(p => p.id === id)
    if (!p) throw new Error('Produto não encontrado')
    return { data: { ...p } }
  },

  async create(data) {
    await delay(500)
    const novo = { ...data, id: _nextId++, ativo: true, data_criacao: new Date().toISOString().slice(0, 10) }
    MOCK_PRODUCTS.push(novo)
    return { data: { ...novo } }
    // return api.post('/api/produtos', data)
  },

  async update(id, data) {
    await delay(400)
    MOCK_PRODUCTS = MOCK_PRODUCTS.map(p => p.id === id ? { ...p, ...data } : p)
    const updated = MOCK_PRODUCTS.find(p => p.id === id)
    return { data: { ...updated } }
    // return api.put(`/api/produtos/${id}`, data)
  },

  async remove(id) {
    await delay(400)
    MOCK_PRODUCTS = MOCK_PRODUCTS.filter(p => p.id !== id)
    return { data: { ok: true } }
    // return api.delete(`/api/produtos/${id}`)
  },

  async toggleAtivo(id) {
    await delay(300)
    MOCK_PRODUCTS = MOCK_PRODUCTS.map(p => p.id === id ? { ...p, ativo: !p.ativo } : p)
    const updated = MOCK_PRODUCTS.find(p => p.id === id)
    return { data: { ...updated } }
  },
}
