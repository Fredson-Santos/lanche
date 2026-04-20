import React, { useEffect, useState, useCallback } from 'react'
import { Card, CardHeader } from '../components/ui/Card'
import { StatCard } from '../components/ui/StatCard'
import { Button } from '../components/ui/Button'
import { Spinner } from '../components/ui/Spinner'
import { reportService } from '../services/reportService'
import { salesService } from '../services/salesService'

const fmtBRL = (v) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
const fmtDateLabel = (iso) => new Date(iso + 'T12:00:00').toLocaleDateString('pt-BR', { day:'2-digit', month:'2-digit' })

const today = new Date()
const toISODate = (d) => d.toISOString().slice(0, 10)
const DEFAULT_INICIO = toISODate(new Date(today.getFullYear(), today.getMonth(), 1))
const DEFAULT_FIM    = toISODate(today)

export function RelatoriosPage() {
  const [inicio, setInicio]   = useState(DEFAULT_INICIO)
  const [fim, setFim]         = useState(DEFAULT_FIM)
  const [vendas, setVendas]   = useState([])
  const [byDay, setByDay]     = useState([])
  const [total, setTotal]     = useState(0)
  const [loading, setLoading] = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    const [vendasResp, faturResp, dayResp] = await Promise.all([
      salesService.getAll({ inicio, fim }),
      reportService.getFaturamento({ inicio, fim }),
      reportService.getVendasPorDia({ inicio, fim }),
    ])
    
    // Filter sales by date on the client side since the backend /api/vendas/ returns all
    const allSales = vendasResp.data || []
    const startObj = new Date(inicio + 'T00:00:00')
    const endObj   = new Date(fim + 'T23:59:59.999')
    const filteredSales = allSales.filter(v => {
      const d = new Date(v.data_venda)
      return d >= startObj && d <= endObj
    })

    setVendas(filteredSales)
    setTotal(faturResp.data.total_faturamento || 0)
    setByDay(dayResp.data.vendas_por_dia || [])
    setLoading(false)
  }, [inicio, fim])

  useEffect(() => { load() }, [load])

  const maxDay = Math.max(...byDay.map(d => d.total), 1)

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Relatórios</h1>
          <p className="page-subtitle">Análise de vendas e faturamento</p>
        </div>
      </div>

      {/* Filters */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: '16px', flexWrap: 'wrap' }}>
          <div className="form-group" style={{ flex: 1, minWidth: 160 }}>
            <label className="form-label">Data Início</label>
            <input
              id="relatorio-inicio"
              type="date"
              className="form-input"
              value={inicio}
              max={fim}
              onChange={e => setInicio(e.target.value)}
            />
          </div>
          <div className="form-group" style={{ flex: 1, minWidth: 160 }}>
            <label className="form-label">Data Fim</label>
            <input
              id="relatorio-fim"
              type="date"
              className="form-input"
              value={fim}
              min={inicio}
              onChange={e => setFim(e.target.value)}
            />
          </div>
          <Button id="btn-relatorio-buscar" variant="primary" onClick={load} loading={loading}>
            🔍 Buscar
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="loading-overlay"><Spinner size="xl" /></div>
      ) : (
        <>
          {/* Summary */}
          <div className="grid grid-3" style={{ marginBottom: '24px' }}>
            <StatCard label="Total de Vendas" value={vendas.length} icon="🛒" accentColor="var(--color-primary)" />
            <StatCard label="Faturamento" value={fmtBRL(total)} icon="💰" accentColor="var(--color-success)" />
            <StatCard label="Ticket Médio" value={vendas.length > 0 ? fmtBRL(total / vendas.length) : 'R$ 0,00'} icon="📊" accentColor="var(--color-info)" />
          </div>

          {/* Daily Chart */}
          {byDay.length > 0 && (
            <Card style={{ marginBottom: '24px' }}>
              <CardHeader title="Vendas por Dia" />
              <div className="chart-container">
                {byDay.map(d => (
                  <div key={d.data} className="chart-bar-group">
                    <div className="chart-bar-value">{fmtBRL(d.total).replace('R$\u00a0', 'R$ ')}</div>
                    <div
                      className="chart-bar"
                      style={{ height: `${Math.max((d.total / maxDay) * 100, 3)}%` }}
                    />
                    <div className="chart-bar-label">{fmtDateLabel(d.data)}</div>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Detail Table */}
          <Card>
            <CardHeader title="Detalhe das Vendas" subtitle={`${vendas.length} venda${vendas.length !== 1 ? 's' : ''} no período`} />
            {vendas.length === 0 ? (
              <div className="empty-state">
                <div className="empty-state-icon">📊</div>
                <p className="empty-state-title">Nenhuma venda encontrada</p>
                <p className="empty-state-text">Ajuste o período e tente novamente.</p>
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
                    {vendas.map(v => (
                      <tr key={v.id}>
                        <td style={{ fontWeight: 600, color: 'var(--color-text-muted)' }}>#{v.id}</td>
                        <td>{new Date(v.data_venda).toLocaleString('pt-BR', { day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit' })}</td>
                        <td>{v.usuario_nome}</td>
                        <td>{v.itens.length} iten{v.itens.length !== 1 ? 's' : ''}</td>
                        <td style={{ fontWeight: 700, color: 'var(--color-success)' }}>{fmtBRL(v.total)}</td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot>
                    <tr>
                      <td colSpan={4} style={{ fontWeight: 700, textAlign: 'right', paddingRight: '20px', color: 'var(--color-text-secondary)' }}>
                        Total do período:
                      </td>
                      <td style={{ fontWeight: 800, fontSize: '1rem', color: 'var(--color-primary)' }}>
                        {fmtBRL(total)}
                      </td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            )}
          </Card>
        </>
      )}
    </div>
  )
}
