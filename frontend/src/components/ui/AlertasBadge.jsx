import React, { useState, useEffect } from 'react'
import { useApi } from '../../hooks/useApi'

/**
 * Componente AlertasBadge - Mostra alertas de validade/temperatura no dashboard
 * RF-01, RF-02, RF-03: Exibe alertas ativos para o usuário
 */
export function AlertasBadge() {
  const { request } = useApi()
  const [alertas, setAlertas] = useState([])
  const [showAlertas, setShowAlertas] = useState(false)
  const [resumo, setResumo] = useState(null)
  const [loading, setLoading] = useState(true)

  // Carrega alertas ao montar o componente
  useEffect(() => {
    carregarAlertas()
    // Recarrega a cada 5 minutos
    const interval = setInterval(carregarAlertas, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  const carregarAlertas = async () => {
    try {
      setLoading(true)
      
      // Carrega resumo de alertas
      const resResumo = await request('/api/alertas/dashboard/resumo', {
        method: 'GET'
      })
      
      if (resResumo.ok) {
        const data = await resResumo.json()
        setResumo(data)
      }
      
      // Carrega lista de alertas
      const resAlertas = await request('/api/alertas/?apenas_ativos=true', {
        method: 'GET'
      })
      
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
        // Remove o alerta da lista
        setAlertas(alertas.filter(a => a.id !== alertaId))
        // Recarrega resumo
        carregarAlertas()
      }
    } catch (error) {
      console.error('Erro ao marcar alerta como lido:', error)
    }
  }

  const getTipoAlertaBadgeColor = (tipo) => {
    switch (tipo) {
      case 'validade':
        return '#FF6B6B' // Vermelho
      case 'temperatura':
        return '#FF9F43' // Laranja
      case 'estoque_minimo':
        return '#FFD93D' // Amarelo
      default:
        return '#999'
    }
  }

  const getTipoAlertaLabel = (tipo) => {
    switch (tipo) {
      case 'validade':
        return 'Validade'
      case 'temperatura':
        return 'Temperatura'
      case 'estoque_minimo':
        return 'Estoque Mínimo'
      default:
        return tipo
    }
  }

  // Se não há alertas, mostra apenas o ícone
  if (!resumo || resumo.total_alertas === 0) {
    return (
      <div className="alertas-badge" title="Nenhum alerta ativo">
        <span className="alertas-icon">🔔</span>
      </div>
    )
  }

  return (
    <div className="alertas-badge-container" style={{ position: 'relative' }}>
      <button
        className="alertas-badge"
        onClick={() => setShowAlertas(!showAlertas)}
        title={`${resumo.total_alertas} alerta${resumo.total_alertas !== 1 ? 's' : ''} ativo${resumo.total_alertas !== 1 ? 's' : ''}`}
      >
        <span className="alertas-icon">⚠️</span>
        <span className="alertas-count">{resumo.total_alertas}</span>
      </button>

      {showAlertas && (
        <div className="alertas-popover">
          <div className="alertas-header">
            <h3>Alertas Ativos ({resumo.total_alertas})</h3>
            <button
              className="alertas-close"
              onClick={() => setShowAlertas(false)}
              style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.2em' }}
            >
              ✕
            </button>
          </div>

          {/* Resumo por tipo */}
          {resumo.alertas_por_tipo && Object.keys(resumo.alertas_por_tipo).length > 0 && (
            <div className="alertas-resumo">
              {Object.entries(resumo.alertas_por_tipo).map(([tipo, count]) => (
                <div key={tipo} className="alertas-tipo-count">
                  <span
                    className="alertas-tipo-badge"
                    style={{ backgroundColor: getTipoAlertaBadgeColor(tipo) }}
                  >
                    {getTipoAlertaLabel(tipo)}
                  </span>
                  <span className="alertas-tipo-number">{count}</span>
                </div>
              ))}
            </div>
          )}

          {/* Lista de alertas */}
          <div className="alertas-lista">
            {loading ? (
              <p style={{ textAlign: 'center', color: '#999' }}>Carregando...</p>
            ) : alertas.length === 0 ? (
              <p style={{ textAlign: 'center', color: '#999' }}>Nenhum alerta</p>
            ) : (
              alertas.slice(0, 5).map(alerta => (
                <div key={alerta.id} className="alerta-item">
                  <div className="alerta-titulo">
                    <span
                      className="alerta-tipo"
                      style={{ backgroundColor: getTipoAlertaBadgeColor(alerta.tipo) }}
                    >
                      {getTipoAlertaLabel(alerta.tipo)}
                    </span>
                    <span className="alerta-texto">{alerta.titulo}</span>
                  </div>
                  {alerta.descricao && (
                    <div className="alerta-descricao">{alerta.descricao}</div>
                  )}
                  <button
                    className="alerta-marcar-lido"
                    onClick={() => marcarComoLido(alerta.id)}
                  >
                    Marcar como lido
                  </button>
                </div>
              ))
            )}
          </div>

          {alertas.length > 5 && (
            <div className="alertas-footer">
              <a href="/alertas" style={{ textDecoration: 'none', color: '#0066CC' }}>
                Ver todos os alertas ({alertas.length})
              </a>
            </div>
          )}
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
          font-size: 1.2em;
          display: flex;
          align-items: center;
          gap: 4px;
          transition: transform 0.2s;
        }

        .alertas-badge:hover {
          transform: scale(1.1);
        }

        .alertas-icon {
          font-size: 1.3em;
        }

        .alertas-count {
          background: #FF6B6B;
          color: white;
          border-radius: 50%;
          width: 20px;
          height: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.75em;
          font-weight: bold;
        }

        .alertas-popover {
          position: absolute;
          top: 100%;
          right: 0;
          background: white;
          border: 1px solid #ddd;
          border-radius: 8px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          width: 350px;
          max-height: 500px;
          display: flex;
          flex-direction: column;
          z-index: 1000;
          margin-top: 8px;
        }

        .alertas-header {
          padding: 12px 16px;
          border-bottom: 1px solid #eee;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .alertas-header h3 {
          margin: 0;
          font-size: 0.95em;
          color: #333;
        }

        .alertas-close {
          color: #999;
          font-size: 1.2em;
          cursor: pointer;
        }

        .alertas-resumo {
          padding: 8px 16px;
          border-bottom: 1px solid #eee;
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }

        .alertas-tipo-count {
          display: flex;
          align-items: center;
          gap: 4px;
          font-size: 0.85em;
        }

        .alertas-tipo-badge {
          padding: 2px 8px;
          border-radius: 4px;
          color: white;
          font-size: 0.75em;
          font-weight: bold;
        }

        .alertas-tipo-number {
          background: #f0f0f0;
          padding: 2px 6px;
          border-radius: 3px;
          font-weight: bold;
          color: #333;
        }

        .alertas-lista {
          flex: 1;
          overflow-y: auto;
          padding: 8px;
        }

        .alerta-item {
          padding: 12px;
          border-bottom: 1px solid #eee;
          border-radius: 4px;
          background: #f9f9f9;
          margin-bottom: 8px;
          font-size: 0.9em;
        }

        .alerta-item:last-child {
          margin-bottom: 0;
          border-bottom: none;
        }

        .alerta-titulo {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 8px;
        }

        .alerta-tipo {
          padding: 3px 8px;
          border-radius: 3px;
          color: white;
          font-size: 0.75em;
          font-weight: bold;
          white-space: nowrap;
        }

        .alerta-texto {
          font-weight: 500;
          color: #333;
          flex: 1;
        }

        .alerta-descricao {
          color: #666;
          font-size: 0.85em;
          margin-bottom: 8px;
          line-height: 1.4;
        }

        .alerta-marcar-lido {
          background: none;
          border: 1px solid #ddd;
          color: #0066CC;
          padding: 4px 8px;
          border-radius: 3px;
          cursor: pointer;
          font-size: 0.8em;
          transition: all 0.2s;
        }

        .alerta-marcar-lido:hover {
          background: #0066CC;
          color: white;
          border-color: #0066CC;
        }

        .alertas-footer {
          padding: 12px 16px;
          border-top: 1px solid #eee;
          text-align: center;
          font-size: 0.9em;
        }
      `}</style>
    </div>
  )
}
