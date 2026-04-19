import React, { useEffect, useState, useCallback } from 'react'
import { useAuth } from '../context/AuthContext'
import { Card, CardHeader } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Spinner } from '../components/ui/Spinner'
import { toast } from '../hooks/useToast'
import { productService } from '../services/productService'
import { salesService } from '../services/salesService'

const fmtBRL = (v) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
const fmtDate = (iso) => new Date(iso).toLocaleString('pt-BR', { day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit' })

const PRODUCT_EMOJI = {
  'X-Burguer': '🍔', 'X-Bacon': '🥓', 'X-Salada': '🥗', 'Hot Dog': '🌭',
  'Batata Pequena': '🍟', 'Batata Grande': '🍟', 'Refrigerante': '🥤',
  'Suco Natural': '🍊', 'Milk shake': '🥛', 'Onion Rings': '🧅',
}
const getEmoji = (nome) => PRODUCT_EMOJI[nome] ?? '🍽️'

export function VendasPage() {
  const { user } = useAuth()

  const [tab, setTab]             = useState('nova') // nova | historico
  const [products, setProducts]   = useState([])
  const [cart, setCart]           = useState([])
  const [search, setSearch]       = useState('')
  const [loading, setLoading]     = useState(true)
  const [finishing, setFinishing] = useState(false)
  const [history, setHistory]     = useState([])
  const [histLoading, setHistLoading] = useState(false)

  const loadProducts = useCallback(async () => {
    const resp = await productService.getAll()
    setProducts(resp.data.filter(p => p.ativo))
    setLoading(false)
  }, [])

  useEffect(() => { loadProducts() }, [loadProducts])

  const loadHistory = useCallback(async () => {
    setHistLoading(true)
    const resp = await salesService.getAll()
    setHistory(resp.data)
    setHistLoading(false)
  }, [])

  useEffect(() => { if (tab === 'historico') loadHistory() }, [tab, loadHistory])

  const filteredProducts = products.filter(p =>
    !search || p.nome.toLowerCase().includes(search.toLowerCase())
  )

  const addToCart = (produto) => {
    setCart(prev => {
      const found = prev.find(i => i.produto_id === produto.id)
      if (found) {
        return prev.map(i => i.produto_id === produto.id
          ? { ...i, quantidade: i.quantidade + 1, subtotal: (i.quantidade + 1) * i.preco_unitario }
          : i
        )
      }
      return [...prev, {
        produto_id:     produto.id,
        nome:          produto.nome,
        preco_unitario: produto.preco,
        quantidade:    1,
        subtotal:      produto.preco,
      }]
    })
  }

  const updateQty = (produto_id, delta) => {
    setCart(prev => prev
      .map(i => i.produto_id === produto_id
        ? { ...i, quantidade: i.quantidade + delta, subtotal: (i.quantidade + delta) * i.preco_unitario }
        : i
      )
      .filter(i => i.quantidade > 0)
    )
  }

  const clearCart = () => setCart([])

  const total = cart.reduce((acc, i) => acc + i.subtotal, 0)

  const handleFinalize = async () => {
    if (cart.length === 0) { toast.error('Carrinho vazio', 'Adicione ao menos um produto.'); return }
    setFinishing(true)
    try {
      const venda = await salesService.create(cart, user.id, user.username)
      toast.success('Venda finalizada!', `Total: ${fmtBRL(venda.data.total)}`)
      clearCart()
      await loadProducts() // refresh stock info
    } catch { toast.error('Erro', 'Não foi possível finalizar a venda.') }
    finally { setFinishing(false) }
  }

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Vendas</h1>
          <p className="page-subtitle">Interface de caixa e histórico de vendas</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button id="tab-nova-venda"  className={`tab-btn ${tab === 'nova'      ? 'active' : ''}`} onClick={() => setTab('nova')}>🛒 Nova Venda</button>
        <button id="tab-historico"   className={`tab-btn ${tab === 'historico' ? 'active' : ''}`} onClick={() => setTab('historico')}>📋 Histórico</button>
      </div>

      {tab === 'nova' && (
        <div className="vendas-layout">
          {/* Products Grid */}
          <div>
            <div style={{ marginBottom: '16px' }}>
              <div className="search-input-wrap">
                <span className="search-icon">🔍</span>
                <input
                  id="venda-search"
                  className="form-input"
                  placeholder="Buscar produto..."
                  value={search}
                  onChange={e => setSearch(e.target.value)}
                  style={{ paddingLeft: '40px' }}
                />
              </div>
            </div>
            {loading ? (
              <div className="loading-overlay"><Spinner size="lg" /></div>
            ) : (
              <div className="products-grid">
                {filteredProducts.map(p => (
                  <div
                    id={`produto-card-${p.id}`}
                    key={p.id}
                    className="product-card-sale"
                    onClick={() => addToCart(p)}
                  >
                    <div className="product-emoji">{getEmoji(p.nome)}</div>
                    <div className="product-name">{p.nome}</div>
                    <div className="product-price">{fmtBRL(p.preco)}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Cart */}
          <div className="cart-card">
            <div className="cart-header">
              <div style={{ fontWeight: 700 }}>🛒 Carrinho</div>
              {cart.length > 0 && (
                <Button variant="ghost" size="sm" onClick={clearCart}>Limpar</Button>
              )}
            </div>

            {cart.length === 0 ? (
              <div className="cart-empty">
                <div className="cart-empty-icon">🛒</div>
                <div>Clique em um produto para adicionar</div>
              </div>
            ) : (
              <div className="cart-items">
                {cart.map(item => (
                  <div key={item.produto_id} className="cart-item">
                    <div className="cart-item-info">
                      <div className="cart-item-name">{item.nome}</div>
                      <div className="cart-item-price">
                        {item.quantidade}x {fmtBRL(item.preco_unitario)} = <strong>{fmtBRL(item.subtotal)}</strong>
                      </div>
                    </div>
                    <div className="cart-qty-ctrl">
                      <button className="cart-qty-btn" onClick={() => updateQty(item.produto_id, -1)}>−</button>
                      <span className="cart-qty-val">{item.quantidade}</span>
                      <button className="cart-qty-btn" onClick={() => updateQty(item.produto_id, +1)}>+</button>
                    </div>
                  </div>
                ))}
              </div>
            )}

            <div className="cart-total">
              <div className="cart-total-row">
                <span>Subtotal</span>
                <span>{fmtBRL(total)}</span>
              </div>
              <div className="cart-total-final">
                <span>Total</span>
                <span>{fmtBRL(total)}</span>
              </div>
            </div>

            <div className="cart-actions">
              <Button
                id="btn-finalizar-venda"
                variant="primary"
                className="w-full"
                onClick={handleFinalize}
                loading={finishing}
                disabled={cart.length === 0}
              >
                ✅ Finalizar Venda
              </Button>
            </div>
          </div>
        </div>
      )}

      {tab === 'historico' && (
        <Card>
          <CardHeader title="Histórico de Vendas" subtitle="Todas as vendas registradas" />
          {histLoading ? (
            <div className="loading-overlay"><Spinner size="lg" /></div>
          ) : history.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">📋</div>
              <p className="empty-state-title">Nenhuma venda registrada ainda</p>
            </div>
          ) : (
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Data/Hora</th>
                    <th>Operador</th>
                    <th>Itens</th>
                    <th>Total</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map(sale => (
                    <tr key={sale.id}>
                      <td style={{ fontWeight: 600, color: 'var(--color-text-muted)' }}>#{sale.id}</td>
                      <td>{fmtDate(sale.data_venda)}</td>
                      <td>{sale.usuario_nome}</td>
                      <td>{sale.itens.length} iten{sale.itens.length !== 1 ? 's' : ''}</td>
                      <td style={{ fontWeight: 700, color: 'var(--color-success)' }}>{fmtBRL(sale.total)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      )}
    </div>
  )
}
