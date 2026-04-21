import React, { useEffect, useState, useCallback } from 'react'
import { useAuth } from '../context/AuthContext'
import { Card, CardHeader } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Spinner } from '../components/ui/Spinner'
import { Modal } from '../components/ui/Modal'
import { toast } from '../hooks/useToast'
import { productService } from '../services/productService'
import { salesService } from '../services/salesService'
import { stockService } from '../services/stockService'
import { useCashier } from '../hooks/useCashier'
import { useOffline } from '../hooks/useOffline'
import { PasswordModal } from '../components/Sales/PasswordModal'
import { OfflineStatusBanner } from '../components/layout/OfflineStatusBanner'

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
  const { isOpen, openCashier, closeCashier, downloadJournal } = useCashier()
  const { logSale, updateSyncStatus, isOnline, downloadJournal: downloadJournalOffline, clearAllSales } = useOffline()

  const [tab, setTab]             = useState('nova') // nova | historico
  const [products, setProducts]   = useState([])
  const [stockInfo, setStockInfo] = useState({})
  const [cart, setCart]           = useState([])
  const [search, setSearch]       = useState('')
  const [loading, setLoading]     = useState(true)
  const [finishing, setFinishing] = useState(false)
  const [history, setHistory]     = useState([])
  const [histLoading, setHistLoading] = useState(false)
  
  // UI for Opening/Closing
  const [showOpenModal, setShowOpenModal]   = useState(false)
  const [showCloseModal, setShowCloseModal] = useState(false)
  const [showDownloadAfterClose, setShowDownloadAfterClose] = useState(false)
  const [authLoading, setAuthLoading]       = useState(false)

  const loadProducts = useCallback(async () => {
    try {
      const [prodResp, stockResp] = await Promise.all([
        productService.getAll(),
        stockService.getAll()
      ])
      
      const sMap = {}
      stockResp.data.forEach(s => {
        sMap[s.produto_id] = s.quantidade
      })
      
      setStockInfo(sMap)
      setProducts(prodResp.data.filter(p => p.ativo))
    } catch {
      toast.error('Erro', 'Falha ao carregar produtos.')
    } finally {
      setLoading(false)
    }
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
    const estoque = stockInfo[produto.id] || 0
    const emCarrinho = cart.find(i => i.produto_id === produto.id)?.quantidade || 0
    
    // Bloquear adição se sem estoque ou não há espaço
    if (estoque === 0) {
      toast.error('Sem Estoque', `${produto.nome} não está disponível.`)
      return
    }
    
    if (emCarrinho >= estoque) {
      toast.warning('Estoque Insuficiente', `Você já tem ${emCarrinho} ${produto.nome} no carrinho. Estoque disponível: ${estoque}`)
      return
    }

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
    const item = cart.find(i => i.produto_id === produto_id)
    if (!item) return

    const novaQtd = item.quantidade + delta
    const estoque = stockInfo[produto_id] || 0

    // Se está tentando aumentar além do estoque
    if (delta > 0 && novaQtd > estoque) {
      toast.warning('Estoque Insuficiente', `Estoque disponível: ${estoque}. Você já tem ${item.quantidade} no carrinho.`)
      return
    }

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
    
    // Preparar dados para backend e log local
    const payload = {
      usuario_id: user.id,
      itens: cart.map(i => ({ 
        produto_id: i.produto_id, 
        quantidade: i.quantidade,
        preco_unitario: i.preco_unitario
      }))
    }

    // 1. REGISTRO LOCAL (AUDITORIA/REDUNDÂNCIA)
    // Mesmo com internet, salvamos localmente primeiro
    let localId = null;
    try {
      localId = await logSale(payload, 'pendente');
    } catch (e) {
      console.error('Erro ao gravar log local:', e);
    }

    try {
      // 2. ENVIO AO SERVIDOR
      const response = await salesService.create(cart, user.id, user.username)
      
      // 3. ATUALIZAR STATUS NO LOG LOCAL
      if (localId) {
        await updateSyncStatus(localId, response.data.id, 'sincronizado');
        console.log('Venda criada e marcada como sincronizada:', { localId, serverId: response.data.id });
      }

      toast.success('Venda finalizada!', `Total: ${fmtBRL(response.data.total)}`)
      clearCart()
      await loadProducts() // refresh stock info
    } catch (err) {
      // Se for erro de rede, o item já está no Log Local como "pendente"
      if (!err.response) {
        toast.warning('Modo Offline', 'Sem conexão com servidor. Venda salva para sincronização futura.');
        clearCart();
        // Otimisticamente tratamos como sucesso no UI do caixa
      } else {
        // Se há erro do servidor, ainda manter no log local como pendente
        console.error('Erro ao finalizar venda:', err.response?.data?.detail || err.message);
        toast.error('Erro', err.response?.data?.detail || 'Não foi possível finalizar a venda.');
      }
    } finally {
      setFinishing(false)
    }
  }

  const handleOpenConfirm = async (password) => {
    setAuthLoading(true)
    const success = await openCashier(password)
    if (success) setShowOpenModal(false)
    setAuthLoading(false)
  }

  const handleCloseConfirm = async (password) => {
    setAuthLoading(true)
    const success = await closeCashier(password)
    if (success) {
      setShowCloseModal(false)
      setShowDownloadAfterClose(true)
    }
    setAuthLoading(false)
  }

  const handleDownloadAndClear = async () => {
    await downloadJournalOffline()
    await clearAllSales()
    setShowDownloadAfterClose(false)
    toast.success('Concluído', 'Arquivo baixado e dados apagados com sucesso.')
  }

  const handleClearOnly = async () => {
    await clearAllSales()
    setShowDownloadAfterClose(false)
    toast.success('Concluído', 'Dados apagados com sucesso.')
  }



  return (
    <div className="animate-fade-in">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 className="page-title">Vendas</h1>
          <p className="page-subtitle">Interface de caixa e histórico de vendas</p>
        </div>
        <div>
          {isOpen ? (
            <Button variant="danger" size="sm" onClick={() => setShowCloseModal(true)}>
              🔓 Fechar Caixa
            </Button>
          ) : (
            <Button variant="success" size="sm" onClick={() => setShowOpenModal(true)}>
              🔒 Abrir Caixa
            </Button>
          )}
        </div>
      </div>
      
      {tab === 'nova' && (
        <div className="vendas-layout-wrapper">
          {/* Overlay bloqueador quando caixa fechado - cobre tudo */}
          {!isOpen && (
            <div className="cashier-lock-overlay-full">
              <div className="cashier-lock-content">
                <div className="cashier-lock-icon">🔒</div>
                <p className="cashier-lock-text">Caixa Fechado</p>
                <p className="cashier-lock-subtitle">Abra o caixa com sua senha para iniciar vendas</p>
                <Button 
                  variant="primary" 
                  size="lg"
                  onClick={() => setShowOpenModal(true)}
                  className="cashier-lock-button"
                >
                  🔓 Abrir Caixa
                </Button>
              </div>
            </div>
          )}

          {isOpen && (
            <>
              <OfflineStatusBanner />

              {/* Tabs */}
              <div className="tabs">
                <button id="tab-nova-venda"  className={`tab-btn ${tab === 'nova'      ? 'active' : ''}`} onClick={() => setTab('nova')}>🛒 Nova Venda</button>
                <button id="tab-historico"   className={`tab-btn ${tab === 'historico' ? 'active' : ''}`} onClick={() => setTab('historico')}>📋 Histórico</button>
              </div>

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
                  disabled={!isOpen}
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
                {filteredProducts.map(p => {
                  const qtd = stockInfo[p.id] || 0
                  const isOutOfStock = qtd === 0
                  
                  return (
                    <div
                      id={`produto-card-${p.id}`}
                      key={p.id}
                      className={`product-card-sale ${isOutOfStock || !isOpen ? 'out-of-stock' : ''}`}
                      onClick={() => !isOutOfStock && isOpen && addToCart(p)}
                      style={isOutOfStock ? { border: '1px solid var(--color-danger)', cursor: 'not-allowed', opacity: 0.6 } : { cursor: 'pointer' }}
                    >
                      <div className="product-emoji">{getEmoji(p.nome)}</div>
                      <div className="product-name">{p.nome}</div>
                      <div style={{ fontSize: '0.75rem', fontWeight: 600, color: isOutOfStock ? 'var(--color-danger)' : 'var(--color-text-muted)', marginBottom: '8px' }}>
                        Estoque: {qtd}
                      </div>
                      <div className="product-price">{fmtBRL(p.preco)}</div>
                    </div>
                  )
                })}
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
                <div>{isOpen ? 'Clique em um produto para adicionar' : 'Abra o caixa para iniciar'}</div>
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
                disabled={cart.length === 0 || !isOpen}
              >
                ✅ Finalizar Venda
              </Button>
            </div>
            </div>
          </div>
            </>
          )}
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
      <PasswordModal 
        isOpen={showOpenModal}
        title="Abertura de Caixa"
        onConfirm={handleOpenConfirm} 
        onCancel={() => setShowOpenModal(false)}
        loading={authLoading}
      />

      <PasswordModal 
        isOpen={showCloseModal}
        title="Fechamento de Caixa"
        onConfirm={handleCloseConfirm}
        onCancel={() => setShowCloseModal(false)}
        loading={authLoading}
      />

      <Modal
        open={showDownloadAfterClose}
        onClose={() => setShowDownloadAfterClose(false)}
        title="Finalizar Turno"
        icon="✅"
        size="md"
        footer={
          <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
            <Button variant="secondary" onClick={handleClearOnly}>
              Não, apenas apagar
            </Button>
            <Button variant="primary" onClick={handleDownloadAndClear}>
              Sim, baixar e apagar
            </Button>
          </div>
        }
      >
        <p>Turno encerrado com sucesso! Deseja baixar o arquivo de auditoria (.json) antes de apagar os dados locais?</p>
      </Modal>
    </div>
  )
}
