import React, { useState, useEffect } from 'react'
import { useApi } from '../hooks/useApi'
import { Table } from '../components/ui/Table'
import { Button } from '../components/ui/Button'
import { Badge } from '../components/ui/Badge'
import { toast } from '../hooks/useToast'

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
        
        if (filtroTipo !== 'todos') {
          data = data.filter(a => a.tipo === filtroTipo)
        }
        
        setAlertas(data)
      }
    } catch (error) {
      console.error('Erro ao carregar alertas:', error)
      toast.error('Erro', 'Erro ao carregar alertas')
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
        toast.success('Pronto', 'Alerta marcado como lido')
        carregarAlertas()
      }
    } catch (error) {
      toast.error('Erro', 'Erro ao marcar alerta como lido')
    }
  }

  const marcarComoResolvido = async (alertaId) => {
    try {
      const res = await request(`/api/alertas/${alertaId}`, {
        method: 'PUT',
        body: JSON.stringify({ ativo: false })
      })
      if (res.ok) {
        toast.success('Pronto', 'Alerta resolvido com sucesso')
        carregarAlertas()
      }
    } catch (error) {
      toast.error('Erro', 'Erro ao resolver alerta')
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

  const columns = [
    { key: 'tipo', label: 'Tipo', width: 150, render: v => getTipoAlertaBadge(v) },
    { key: 'titulo', label: 'Alerta', render: (_, r) => (
      <div>
        <div style={{ fontWeight: 500 }}>{r.titulo}</div>
        {r.descricao && <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>{r.descricao}</div>}
      </div>
    )},
    { key: 'data_criacao', label: 'Data', width: 150, render: v => new Date(v).toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' }) },
    { key: 'status', label: 'Status', width: 120, render: (_, r) => (
      !r.lido ? <Badge variant="danger">Não lido</Badge> : <Badge variant="success">Lido</Badge>
    )}
  ]

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Alertas do Sistema</h1>
          <p className="page-subtitle">Visualize e resolva as pendências de validade e temperatura</p>
        </div>
      </div>

      <div className="search-bar" style={{ marginBottom: '24px', display: 'flex', gap: '24px', flexWrap: 'wrap' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <label style={{ fontWeight: 500, fontSize: '0.875rem' }}>Exibir:</label>
          <select
            className="form-select"
            value={filtroLido}
            onChange={(e) => setFiltroLido(e.target.value)}
            style={{ width: '160px' }}
          >
            <option value="nao-lidos">Não lidos</option>
            <option value="todos">Todos</option>
          </select>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <label style={{ fontWeight: 500, fontSize: '0.875rem' }}>Tipo:</label>
          <select
            className="form-select"
            value={filtroTipo}
            onChange={(e) => setFiltroTipo(e.target.value)}
            style={{ width: '180px' }}
          >
            <option value="todos">Todos os tipos</option>
            <option value="validade">Validade</option>
            <option value="temperatura">Temperatura</option>
            <option value="estoque_minimo">Estoque Mínimo</option>
          </select>
        </div>
      </div>

      <Table
        columns={columns}
        data={alertas}
        loading={loading}
        emptyMessage="✅ Nenhum alerta encontrado no momento."
        actions={(row) => (
          <div style={{ display: 'flex', gap: '8px' }}>
            {!row.lido && (
              <Button variant="ghost" size="sm" onClick={() => marcarComoLido(row.id)}>
                👀 Marcar Lido
              </Button>
            )}
            <Button variant="success" size="sm" onClick={() => marcarComoResolvido(row.id)}>
              ✓ Resolver
            </Button>
          </div>
        )}
      />
    </div>
  )
}
