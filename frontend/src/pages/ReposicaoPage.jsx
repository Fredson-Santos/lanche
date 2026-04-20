import React, { useState, useEffect, useCallback } from 'react'
import { useApi } from '../hooks/useApi'
import { useAuth } from '../context/AuthContext'
import { Table } from '../components/ui/Table'
import { Button } from '../components/ui/Button'
import { Badge } from '../components/ui/Badge'
import { StatCard } from '../components/ui/StatCard'
import { toast } from '../hooks/useToast'

export function ReposicaoPage() {
  const { request } = useApi()
  const { hasRole } = useAuth()
  const canManage = hasRole('admin', 'gerente')

  const [ordens, setOrdens] = useState([])
  const [loading, setLoading] = useState(true)
  const [filtroStatus, setFiltroStatus] = useState('todos')
  const [resumo, setResumo] = useState(null)

  const carregarOrdens = useCallback(async () => {
    try {
      setLoading(true)
      let url = '/api/reposicao/'
      
      if (filtroStatus !== 'todos') {
        url += `?status_filtro=${filtroStatus}`
      }
      
      const res = await request(url, { method: 'GET' })
      
      if (res.ok) {
        let data = await res.json()
        setOrdens(Array.isArray(data) ? data : [])
      }
    } catch (error) {
      console.error('Erro ao carregar ordens:', error)
      toast.error('Erro ao carregar ordens', 'Não foi possível carregar as ordens de reposição.')
    } finally {
      setLoading(false)
    }
  }, [filtroStatus, request])

  const carregarResumo = useCallback(async () => {
    try {
      const res = await request('/api/reposicao/dashboard/resumo', { method: 'GET' })
      if (res.ok) {
        const data = await res.json()
        setResumo(data)
      }
    } catch (error) {
      console.error('Erro ao carregar resumo:', error)
    }
  }, [request])

  useEffect(() => {
    carregarOrdens()
    carregarResumo()
  }, [carregarOrdens, carregarResumo])

  const confirmarOrdem = async (ordemId) => {
    if (!canManage) return toast.error('Acesso Negado', 'Você não tem permissão para confirmar ordens.')
    try {
      const res = await request(`/api/reposicao/${ordemId}/confirmar`, { method: 'PUT' })
      if (res.ok) {
        toast.success('Ordem confirmada', 'A ordem foi movida para o status Confirmada.')
        carregarOrdens()
        carregarResumo()
      } else {
        toast.error('Erro', 'Não foi possível confirmar a ordem.')
      }
    } catch (error) {
      toast.error('Erro', 'Ocorreu um erro na solicitação.')
    }
  }

  const receberOrdem = async (ordemId, quantidadeRecebida) => {
    if (!canManage) return toast.error('Acesso Negado', 'Você não tem permissão.')
    try {
      const res = await request(`/api/reposicao/${ordemId}/receber?quantidade_recebida=${quantidadeRecebida}`, { method: 'PUT' })
      if (res.ok) {
        toast.success('Recebimento registrado', 'Estoque atualizado com sucesso.')
        carregarOrdens()
        carregarResumo()
      } else {
        toast.error('Erro', 'Não foi possível registrar o recebimento.')
      }
    } catch (error) {
      toast.error('Erro', 'Ocorreu um erro na solicitação.')
    }
  }

  const cancelarOrdem = async (ordemId) => {
    if (!canManage) return toast.error('Acesso Negado', 'Você não tem permissão.')
    if (window.confirm('Tem certeza que deseja cancelar esta ordem?')) {
      try {
        const res = await request(`/api/reposicao/${ordemId}?motivo=Cancelada pelo usuário`, { method: 'DELETE' })
        if (res.ok) {
          toast.success('Ordem cancelada', 'A ordem foi cancelada com sucesso.')
          carregarOrdens()
          carregarResumo()
        } else {
          toast.error('Erro', 'Não foi possível cancelar a ordem.')
        }
      } catch (error) {
        toast.error('Erro', 'Ocorreu um erro na solicitação.')
      }
    }
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'pendente':   return <Badge variant="warning" dot>Pendente</Badge>
      case 'confirmada': return <Badge variant="info" dot>Confirmada</Badge>
      case 'recebida':   return <Badge variant="success" dot>Recebida</Badge>
      case 'cancelada':  return <Badge variant="danger" dot>Cancelada</Badge>
      default:           return <Badge variant="default">{status}</Badge>
    }
  }

  const columns = [
    { key: 'id', label: 'ID', width: 60, render: v => <span style={{ color: 'var(--color-text-muted)' }}>#{v}</span> },
    { key: 'produto', label: 'Produto', render: (_, r) => (
      <div>
        <div style={{ fontWeight: 500 }}>{r.produto?.nome || `Produto ID: ${r.produto_id}`}</div>
        <div style={{ fontSize: '0.78rem', color: 'var(--color-text-muted)' }}>Motivo: {r.motivo || 'N/A'}</div>
      </div>
    )},
    { key: 'quantidades', label: 'Quantidades', render: (_, r) => (
      <div style={{ display: 'flex', gap: '16px' }}>
        <div>
          <span style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', display: 'block' }}>Solicitado</span>
          <strong style={{ fontSize: '0.9rem' }}>{r.quantidade_solicitada}</strong>
        </div>
        <div>
          <span style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', display: 'block' }}>Recebido</span>
          <strong style={{ fontSize: '0.9rem', color: r.quantidade_recebida > 0 ? 'var(--color-success)' : 'inherit' }}>
            {r.quantidade_recebida || 0}
          </strong>
        </div>
      </div>
    )},
    { key: 'status', label: 'Status', render: v => getStatusBadge(v) },
    { key: 'data_criacao', label: 'Criada Em', render: v => new Date(v).toLocaleDateString('pt-BR') },
  ]

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Gerenciamento de Reposição</h1>
          <p className="page-subtitle">Visualize e gerencie ordens de reposição automática de estoque</p>
        </div>
      </div>

      {resumo && (
        <div className="grid grid-3" style={{ marginBottom: '32px' }}>
          <StatCard
            label="Pendentes / Confirmadas"
            value={resumo.ordens_pendentes}
            icon="⏳"
            accentColor="var(--color-warning)"
          />
          <StatCard
            label="Recebidas (7 dias)"
            value={resumo.ordens_recebidas_7dias}
            icon="✅"
            accentColor="var(--color-success)"
          />
          <StatCard
            label="Quantidade Pendente"
            value={resumo.quantidade_total_pendente}
            icon="📦"
            accentColor="var(--color-info)"
          />
        </div>
      )}

      {/* Filters */}
      <div className="search-bar" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <label style={{ fontWeight: 500, fontSize: '0.875rem' }}>Filtrar Status:</label>
          <select
            className="form-select"
            value={filtroStatus}
            onChange={(e) => setFiltroStatus(e.target.value)}
            style={{ width: '200px' }}
          >
            <option value="todos">Todos os status</option>
            <option value="pendente">Pendente</option>
            <option value="confirmada">Confirmada</option>
            <option value="recebida">Recebida</option>
            <option value="cancelada">Cancelada</option>
          </select>
        </div>
      </div>

      <Table
        columns={columns}
        data={ordens}
        loading={loading}
        emptyMessage="Nenhuma ordem encontrada."
        actions={(row) => (
          <div style={{ display: 'flex', gap: '8px' }}>
            {row.status === 'pendente' && (
              <>
                <Button variant="primary" size="sm" onClick={() => confirmarOrdem(row.id)}>
                  ✓ Confirmar
                </Button>
                <Button variant="danger" size="sm" onClick={() => cancelarOrdem(row.id)}>
                  ✕ Cancelar
                </Button>
              </>
            )}
            {row.status === 'confirmada' && (
               <Button variant="success" size="sm" onClick={() => receberOrdem(row.id, row.quantidade_solicitada)}>
                 📦 Receber
               </Button>
            )}
            {row.observacoes && (
              <Button variant="ghost" size="sm" onClick={() => alert(`Observações: ${row.observacoes}`)}>
                📝 Info
              </Button>
            )}
          </div>
        )}
      />
    </div>
  )
}
