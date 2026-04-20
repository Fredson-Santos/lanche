import React, { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { StatCard } from '../components/ui/StatCard'
import { Card, CardHeader } from '../components/ui/Card'
import { Badge, ActiveBadge } from '../components/ui/Badge'
import { Spinner } from '../components/ui/Spinner'
import { productService } from '../services/productService'
import { stockService } from '../services/stockService'
import { salesService } from '../services/salesService'

const fmtBRL = (v) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
const fmtDate = (iso) => new Date(iso).toLocaleDateString('pt-BR', { day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit' })

export function DashboardPage() {
  const { user } = useAuth()
  const [stats, setStats]       = useState(null)
  const [recentSales, setRecent] = useState([])
  const [lowStock, setLowStock] = useState([])
  const [loading, setLoading]   = useState(true)

  useEffect(() => {
    async function load() {
      const [prodResp, stockResp, todayResp, salesResp] = await Promise.all([
        productService.getAll(),
        stockService.getAll(),
        salesService.getToday(),
        salesService.getAll(),
      ])

      const produtos = prodResp.data
      const estoque  = stockResp.data
      const today    = todayResp.data
      const allSales = salesResp.data

      const mappedEstoque = estoque.map(s => ({
        ...s,
        nome: s.produto?.nome || 'Sem nome'
      }))

      setStats({
        totalProdutos: produtos.filter(p => p.ativo).length,
        vendasHoje:    today.count,
        faturamentoHoje: today.total,
        estoqueAlerta: mappedEstoque.filter(e => e.quantidade < 10).length,
      })
      setRecent(allSales.slice(0, 5).sort((a, b) => b.id - a.id))
      setLowStock(mappedEstoque.filter(e => e.quantidade < 10).slice(0, 5))
      setLoading(false)
    }
    load()
  }, [])

  if (loading) return (
    <div className="loading-overlay">
      <Spinner size="xl" />
      <span>Carregando dashboard...</span>
    </div>
  )

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Olá, {user?.username} 👋</h1>
          <p className="page-subtitle">Aqui está o resumo de hoje — {new Date().toLocaleDateString('pt-BR', { weekday:'long', day:'2-digit', month:'long', year:'numeric' })}</p>
        </div>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-4" style={{ marginBottom: '32px' }}>
        <StatCard
          label="Vendas Hoje"
          value={stats.vendasHoje}
          icon="🛒"
          accentColor="var(--color-primary)"
        />
        <StatCard
          label="Faturamento Hoje"
          value={fmtBRL(stats.faturamentoHoje)}
          icon="💰"
          accentColor="var(--color-success)"
        />
        <StatCard
          label="Produtos Ativos"
          value={stats.totalProdutos}
          icon="🍔"
          accentColor="var(--color-info)"
        />
        <StatCard
          label="Estoque em Alerta"
          value={stats.estoqueAlerta}
          icon="⚠️"
          accentColor="var(--color-warning)"
        />
      </div>

      {/* Bottom Grid */}
      <div className="grid grid-2">
        {/* Recent Sales */}
        <Card>
          <CardHeader title="Últimas Vendas" subtitle="Histórico recente" />
          {recentSales.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">🛒</div>
              <p className="empty-state-title">Nenhuma venda ainda hoje</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {recentSales.map(sale => (
                <div key={sale.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 0', borderBottom: '1px solid var(--color-border)' }}>
                  <div>
                    <div style={{ fontSize: '0.875rem', fontWeight: 600 }}>Venda #{sale.id}</div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--color-text-muted)' }}>
                      {fmtDate(sale.data_venda)} · {sale.usuario_nome}
                    </div>
                  </div>
                  <div style={{ fontWeight: 700, color: 'var(--color-success)' }}>{fmtBRL(sale.total)}</div>
                </div>
              ))}
            </div>
          )}
        </Card>

        {/* Low Stock */}
        <Card>
          <CardHeader title="Alertas de Estoque" subtitle="Produtos com quantidade baixa" />
          {lowStock.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">✅</div>
              <p className="empty-state-title">Estoque em dia!</p>
              <p className="empty-state-text">Todos os produtos têm quantidade adequada.</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {lowStock.map(item => (
                <div key={item.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 0', borderBottom: '1px solid var(--color-border)' }}>
                  <div style={{ fontSize: '0.875rem', fontWeight: 500 }}>{item.nome}</div>
                  <Badge variant={item.quantidade === 0 ? 'danger' : 'warning'} dot>
                    {item.quantidade === 0 ? 'Sem estoque' : `${item.quantidade} unid.`}
                  </Badge>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}
