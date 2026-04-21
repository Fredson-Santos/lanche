import React, { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { StatCard } from '../components/ui/StatCard'
import { Card, CardHeader } from '../components/ui/Card'
import { Badge, ActiveBadge } from '../components/ui/Badge'
import { Spinner } from '../components/ui/Spinner'
import { productService } from '../services/productService'
import { stockService } from '../services/stockService'
import { salesService } from '../services/salesService'
import api from '../services/api'

const fmtBRL = (v) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
const fmtDate = (iso) => new Date(iso).toLocaleDateString('pt-BR', { day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit' })

export function DashboardPage() {
  const { user } = useAuth()
  const canSeeAlerts = user?.role === 'admin' || user?.role === 'gerente'

  const [stats, setStats]       = useState(null)
  const [recentSales, setRecent] = useState([])
  const [alerts, setAlerts]     = useState([])
  const [loading, setLoading]   = useState(true)

  useEffect(() => {
    async function load() {
      const promises = [
        productService.getAll(),
        stockService.getAll(),
        salesService.getToday(),
        salesService.getAll(),
      ]

      // Apenas busca alertas se tiver permissão
      if (canSeeAlerts) {
        promises.push(api.get('/api/alertas/dashboard/resumo').catch(() => ({ data: { total_nao_lidos: 0 } })))
        promises.push(api.get('/api/alertas/?apenas_ativos=true').catch(() => ({ data: [] })))
      }

      const results = await Promise.all(promises)
      
      const prodResp  = results[0]
      const stockResp = results[1]
      const todayResp = results[2]
      const salesResp = results[3]
      
      const produtos = prodResp.data
      const today    = todayResp.data
      const allSales = salesResp.data
      
      let resumoAlertas = { total_nao_lidos: 0 }
      let alertasNaoLidos = []

      if (canSeeAlerts) {
        resumoAlertas = results[4]?.data || resumoAlertas
        alertasNaoLidos = results[5]?.data || alertasNaoLidos
      }

      setStats({
        totalProdutos: produtos.filter(p => !!p.ativo).length,
        vendasHoje:    today.count,
        faturamentoHoje: today.total,
        alertasSistema: resumoAlertas.total_nao_lidos,
      })
      setRecent(allSales.slice(0, 5).sort((a, b) => b.id - a.id))
      setAlerts(alertasNaoLidos.slice(0, 5))
      setLoading(false)
    }
    load()
  }, [canSeeAlerts])

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
      <div className={`grid ${canSeeAlerts ? 'grid-4' : 'grid-3'}`} style={{ marginBottom: '32px' }}>
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
        {canSeeAlerts && (
          <StatCard
            label="Alertas Novos"
            value={stats.alertasSistema}
            icon="⚠️"
            accentColor="var(--color-warning)"
          />
        )}
      </div>

      {/* Bottom Grid */}
      <div className={`grid ${canSeeAlerts ? 'grid-2' : 'grid-1'}`}>
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

        {/* Central de Alertas - Apenas para Gerentes/Admins */}
        {canSeeAlerts && (
          <Card>
            <CardHeader title="Central de Alertas" subtitle="Últimas pendências" />
            {alerts.length === 0 ? (
              <div className="empty-state">
                <div className="empty-state-icon">✅</div>
                <p className="empty-state-title">Tudo em dia!</p>
                <p className="empty-state-text">Nenhum alerta ativo no momento.</p>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {alerts.map(alerta => (
                  <div 
                    key={alerta.id} 
                    style={{ 
                      display: 'flex', 
                      justifyContent: 'space-between', 
                      alignItems: 'center', 
                      padding: '10px 0', 
                      borderBottom: '1px solid var(--color-border)',
                      opacity: alerta.lido ? 0.7 : 1 
                    }}
                  >
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{ fontSize: '0.875rem', fontWeight: 600 }}>{alerta.titulo}</div>
                        {!alerta.lido && <Badge variant="danger" style={{ padding: '2px 6px', fontSize: '0.65rem' }}>NOVO</Badge>}
                      </div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>
                        {new Date(alerta.data_criacao).toLocaleDateString('pt-BR')}
                      </div>
                    </div>
                    <Badge variant={alerta.tipo === 'validade' ? 'danger' : alerta.tipo === 'temperatura' ? 'warning' : 'info'} dot>
                      {alerta.tipo === 'validade' ? 'Validade' : alerta.tipo === 'temperatura' ? 'Temp.' : 'Estoque'}
                    </Badge>
                  </div>
                ))}
              </div>
            )}
          </Card>
        )}
      </div>
    </div>
  )
}
