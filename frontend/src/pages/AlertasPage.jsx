import React, { useState, useEffect } from 'react'
import { useApi } from '../hooks/useApi'

/**
 * Página de Alertas - Exibe todos os alertas do sistema
 * RF-01, RF-02, RF-03: Alertas de validade, temperatura e estoque mínimo
 */
export function AlertasPage() {
  const { request } = useApi()
  const [alertas, setAlertas] = useState([])
  const [loading, setLoading] = useState(true)
  const [filtroTipo, setFiltroTipo] = useState('todos')
  const [filtroLido, setFiltroLido] = useState('nao-lidos')
  const [mensagem, setMensagem] = useState('')

  useEffect(() => {
    carregarAlertas()
  }, [filtroTipo, filtroLido])

  const carregarAlertas = async () => {
    try {
      setLoading(true)
      let url = '/api/alertas/?apenas_ativos='
      
      if (filtroLido === 'todos') {
        url = '/api/alertas/?apenas_ativos=false'
      } else if (filtroLido === 'nao-lidos') {
        url = '/api/alertas/?apenas_ativos=true'
      }
      
      const res = await request(url, { method: 'GET' })
      
      if (res.ok) {
        let data = await res.json()
        data = Array.isArray(data) ? data : []
        
        // Filtra por tipo
        if (filtroTipo !== 'todos') {
          data = data.filter(a => a.tipo === filtroTipo)
        }
        
        setAlertas(data)
      }
    } catch (error) {
      console.error('Erro ao carregar alertas:', error)
      setMensagem('Erro ao carregar alertas')
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
        setMensagem('Alerta marcado como lido')
        setTimeout(() => {
          setMensagem('')
          carregarAlertas()
        }, 2000)
      }
    } catch (error) {
      console.error('Erro:', error)
      setMensagem('Erro ao marcar alerta como lido')
    }
  }

  const marcarComoResolvido = async (alertaId) => {
    try {
      const res = await request(`/api/alertas/${alertaId}`, {
        method: 'PUT',
        body: JSON.stringify({ ativo: false })
      })
      
      if (res.ok) {
        setMensagem('Alerta marcado como resolvido')
        setTimeout(() => {
          setMensagem('')
          carregarAlertas()
        }, 2000)
      }
    } catch (error) {
      console.error('Erro:', error)
      setMensagem('Erro ao resolver alerta')
    }
  }

  const getTipoAlertaBadgeColor = (tipo) => {
    switch (tipo) {
      case 'validade':
        return '#FF6B6B'
      case 'temperatura':
        return '#FF9F43'
      case 'estoque_minimo':
        return '#FFD93D'
      default:
        return '#999'
    }
  }

  const getTipoAlertaLabel = (tipo) => {
    switch (tipo) {
      case 'validade':
        return '📅 Validade'
      case 'temperatura':
        return '🌡️ Temperatura'
      case 'estoque_minimo':
        return '📦 Estoque Mínimo'
      default:
        return tipo
    }
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Alertas do Sistema</h1>
        <p>Visualize todos os alertas de validade, temperatura e estoque</p>
      </div>

      {mensagem && (
        <div style={{
          padding: '12px 16px',
          marginBottom: '16px',
          backgroundColor: '#D4EDDA',
          color: '#155724',
          borderRadius: '4px',
          border: '1px solid #C3E6CB'
        }}>
          {mensagem}
        </div>
      )}

      <div className="alertas-filtros" style={{
        display: 'flex',
        gap: '16px',
        marginBottom: '24px',
        flexWrap: 'wrap'
      }}>
        <div>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
            Filtrar por tipo:
          </label>
          <select
            value={filtroTipo}
            onChange={(e) => setFiltroTipo(e.target.value)}
            style={{
              padding: '8px 12px',
              borderRadius: '4px',
              border: '1px solid #ddd',
              backgroundColor: 'white',
              cursor: 'pointer'
            }}
          >
            <option value="todos">Todos os tipos</option>
            <option value="validade">📅 Validade</option>
            <option value="temperatura">🌡️ Temperatura</option>
            <option value="estoque_minimo">📦 Estoque Mínimo</option>
          </select>
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
            Filtrar por status:
          </label>
          <select
            value={filtroLido}
            onChange={(e) => setFiltroLido(e.target.value)}
            style={{
              padding: '8px 12px',
              borderRadius: '4px',
              border: '1px solid #ddd',
              backgroundColor: 'white',
              cursor: 'pointer'
            }}
          >
            <option value="nao-lidos">Não lidos</option>
            <option value="todos">Todos</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '32px' }}>
          <p>Carregando alertas...</p>
        </div>
      ) : alertas.length === 0 ? (
        <div style={{
          textAlign: 'center',
          padding: '32px',
          backgroundColor: '#F9F9F9',
          borderRadius: '8px',
          border: '1px solid #eee'
        }}>
          <p style={{ fontSize: '1.1em', color: '#666' }}>
            ✅ Nenhum alerta no momento
          </p>
        </div>
      ) : (
        <div className="alertas-grid" style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
          gap: '16px'
        }}>
          {alertas.map(alerta => (
            <div
              key={alerta.id}
              style={{
                backgroundColor: '#fff',
                border: `2px solid ${getTipoAlertaBadgeColor(alerta.tipo)}`,
                borderRadius: '8px',
                padding: '16px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              }}
            >
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginBottom: '12px'
              }}>
                <span
                  style={{
                    backgroundColor: getTipoAlertaBadgeColor(alerta.tipo),
                    color: 'white',
                    padding: '4px 12px',
                    borderRadius: '20px',
                    fontSize: '0.9em',
                    fontWeight: 'bold',
                    whiteSpace: 'nowrap'
                  }}
                >
                  {getTipoAlertaLabel(alerta.tipo)}
                </span>
                {!alerta.lido && (
                  <span style={{
                    backgroundColor: '#FF6B6B',
                    color: 'white',
                    padding: '2px 8px',
                    borderRadius: '3px',
                    fontSize: '0.75em',
                    fontWeight: 'bold'
                  }}>
                    NOVO
                  </span>
                )}
              </div>

              <h3 style={{
                margin: '0 0 8px 0',
                color: '#333',
                fontSize: '1em'
              }}>
                {alerta.titulo}
              </h3>

              {alerta.descricao && (
                <p style={{
                  margin: '0 0 12px 0',
                  color: '#666',
                  fontSize: '0.9em',
                  lineHeight: '1.4'
                }}>
                  {alerta.descricao}
                </p>
              )}

              <div style={{
                fontSize: '0.85em',
                color: '#999',
                marginBottom: '12px'
              }}>
                Criado em: {new Date(alerta.data_criacao).toLocaleDateString('pt-BR', {
                  day: '2-digit',
                  month: '2-digit',
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </div>

              <div style={{
                display: 'flex',
                gap: '8px'
              }}>
                {!alerta.lido && (
                  <button
                    onClick={() => marcarComoLido(alerta.id)}
                    style={{
                      flex: 1,
                      padding: '8px 12px',
                      backgroundColor: '#0066CC',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      fontSize: '0.9em',
                      fontWeight: 'bold',
                      transition: 'background 0.2s'
                    }}
                    onMouseOver={(e) => e.target.style.backgroundColor = '#0052A3'}
                    onMouseOut={(e) => e.target.style.backgroundColor = '#0066CC'}
                  >
                    ✓ Marcar como lido
                  </button>
                )}
                <button
                  onClick={() => marcarComoResolvido(alerta.id)}
                  style={{
                    flex: 1,
                    padding: '8px 12px',
                    backgroundColor: '#28A745',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '0.9em',
                    fontWeight: 'bold',
                    transition: 'background 0.2s'
                  }}
                  onMouseOver={(e) => e.target.style.backgroundColor = '#218838'}
                  onMouseOut={(e) => e.target.style.backgroundColor = '#28A745'}
                >
                  ✓ Resolver
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
