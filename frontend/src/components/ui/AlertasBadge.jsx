import React, { useState, useEffect } from 'react'
import { useApi } from '../../hooks/useApi'
import { Badge } from './Badge'
import { Button } from './Button'
import { useNavigate } from 'react-router-dom'

/**
 * Componente AlertasBadge - Mostra alertas de validade/temperatura no dashboard
 * RF-01, RF-02, RF-03: Exibe alertas ativos para o usuário
 */
export function AlertasBadge() {
  const { request } = useApi()
  const navigate = useNavigate()
  const [alertas, setAlertas] = useState([])
  const [showAlertas, setShowAlertas] = useState(false)
  const [resumo, setResumo] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    carregarAlertas()
    const interval = setInterval(carregarAlertas, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  const carregarAlertas = async () => {
    try {
      setLoading(true)
      const resResumo = await request('/api/alertas/dashboard/resumo', { method: 'GET' })
      if (resResumo.ok) {
        setResumo(await resResumo.json())
      }
      
      const resAlertas = await request('/api/alertas/?apenas_ativos=true', { method: 'GET' })
      if (resAlertas.ok) {
        const data = await resAlertas.json()
        setAlertas(Array.isArray(data) ? data : [])
      }
    } catch (error) {
      console.error('Erro ao carregar alertas:', error)
    } finally {
      setLoading(false)
    }
  }

  const marcarComoLido = async (alertaId) => {
    try {
      const res = await request(`/api/alertas/${alertaId}`, {
        method: 'PUT',
        body: JSON.stringify({ lido: true })
      })
      if (res.ok) {
        setAlertas(alertas.filter(a => a.id !== alertaId))
        carregarAlertas()
      }
    } catch (error) {
      console.error('Erro ao marcar alerta como lido:', error)
    }
  }

  const getTipoAlertaBadge = (tipo) => {
    switch (tipo) {
      case 'validade': return <Badge variant="danger" dot>Validade</Badge>
      case 'temperatura': return <Badge variant="warning" dot>Temperatura</Badge>
      case 'estoque_minimo': return <Badge variant="info" dot>Estoque Mínimo</Badge>
      default: return <Badge variant="default">{tipo}</Badge>
    }
  }

  const hasAlerts = resumo && resumo.total_nao_lidos > 0

  return (
    <div className="alertas-badge-container" style={{ position: 'relative' }}>
      <button
        className="alertas-badge"
        onClick={(e) => { e.stopPropagation(); setShowAlertas(!showAlertas); }}
        title={hasAlerts ? `${resumo.total_nao_lidos} nova(s) notificação(ões)` : 'Nenhum alerta novo'}
      >
        <span className="alertas-icon">{hasAlerts ? '⚠️' : '🔔'}</span>
        {hasAlerts && <span className="alertas-count">{resumo.total_nao_lidos}</span>}
      </button>

      {showAlertas && hasAlerts && (
        <div className="alertas-popover animate-fade-in" onClick={(e) => e.stopPropagation()}>
          <div className="alertas-header">
            <h3 style={{ margin: 0, fontWeight: 600 }}>Alertas Ativos ({resumo.total_alertas})</h3>
            <button className="alertas-close" onClick={() => setShowAlertas(false)}>✕</button>
          </div>

          <div className="alertas-lista">
            {loading ? (
              <p style={{ textAlign: 'center', color: 'var(--color-text-muted)' }}>Buscando alertas...</p>
            ) : alertas.length === 0 ? (
              <p style={{ textAlign: 'center', color: 'var(--color-text-muted)' }}>✅ Todos os alertas foram lidos.</p>
            ) : (
              alertas.slice(0, 5).map(alerta => (
                <div key={alerta.id} className="alerta-item">
                  <div className="alerta-titulo" style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                    {getTipoAlertaBadge(alerta.tipo)}
                    <span style={{ fontWeight: 500, flex: 1, fontSize: '0.9rem' }}>{alerta.titulo}</span>
                  </div>
                  {alerta.descricao && (
                    <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)', marginBottom: '12px' }}>
                      {alerta.descricao}
                    </div>
                  )}
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    onClick={(e) => { e.stopPropagation(); marcarComoLido(alerta.id); }} 
                    style={{ width: '100%', fontSize: '0.8rem' }}
                  >
                    Marcar como lido
                  </Button>
                </div>
              ))
            )}
          </div>

          <div className="alertas-footer">
            <Button variant="primary" style={{ width: '100%' }} onClick={() => { setShowAlertas(false); navigate('/alertas') }}>
              Ver todos os {alertas.length} alertas
            </Button>
          </div>
        </div>
      )}

      <style>{`
        .alertas-badge-container {
          position: relative;
        }

        .alertas-badge {
          background: none;
          border: none;
          cursor: pointer;
          position: relative;
          padding: 8px 12px;
          display: flex;
          align-items: center;
          gap: 4px;
          transition: transform 0.2s;
          color: var(--color-text-primary);
        }

        .alertas-badge:hover {
          transform: scale(1.05);
        }

        .alertas-icon {
          font-size: 1.3em;
        }

        .alertas-count {
          background: var(--color-danger);
          color: white;
          border-radius: 50%;
          width: 20px;
          height: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.75rem;
          font-weight: 700;
          position: absolute;
          top: 0;
          right: 4px;
          border: 2px solid var(--color-bg);
        }

        .alertas-popover {
          position: absolute;
          top: 100%;
          right: 0;
          background-color: var(--color-bg-card);
          border: 1px solid var(--color-border);
          border-radius: 12px;
          box-shadow: 0 12px 32px rgba(0, 0, 0, 0.7);
          width: 360px;
          max-height: 500px;
          display: flex;
          flex-direction: column;
          z-index: 1000;
          margin-top: 16px;
          overflow: hidden;
        }

        .alertas-header {
          padding: 16px;
          border-bottom: 1px solid var(--color-border);
          display: flex;
          justify-content: space-between;
          align-items: center;
          background: rgba(255, 255, 255, 0.03);
          color: var(--color-text-primary);
        }

        .alertas-close {
          background: none;
          border: none;
          cursor: pointer;
          color: var(--color-text-muted);
          font-size: 1.2rem;
          padding: 4px;
        }

        .alertas-close:hover {
          color: var(--color-text-primary);
        }

        .alertas-lista {
          flex: 1;
          overflow-y: auto;
          padding: 12px;
          display: flex;
          flex-direction: column;
          gap: 8px;
          color: var(--color-text-primary);
        }

        .alerta-item {
          padding: 16px;
          border: 1px solid var(--color-border);
          border-radius: 8px;
          background: rgba(255, 255, 255, 0.02);
        }

        .alertas-footer {
          padding: 16px;
          border-top: 1px solid var(--color-border);
          background: rgba(0, 0, 0, 0.2);
        }
      `}</style>
    </div>
  )
}
