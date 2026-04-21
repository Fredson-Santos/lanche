import React, { useState, useEffect } from 'react'
import { useApi } from '../hooks/useApi'
import { Table } from '../components/ui/Table'
import { Button } from '../components/ui/Button'
import { Badge } from '../components/ui/Badge'
import { Modal } from '../components/ui/Modal'
import { Input } from '../components/ui/Input'
import { toast } from '../hooks/useToast'

/**
 * Página de Gerenciamento de Chaves de API
 * Permite que administradores gerem tokens de acesso para parceiros externos.
 */
export function ApiKeysPage() {
  const { request } = useApi()
  const [keys, setKeys] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showSuccessModal, setShowSuccessModal] = useState(false)
  const [newKeyData, setNewKeyData] = useState(null)
  const [isCopying, setIsCopying] = useState(false)
  
  // Form state
  const [form, setForm] = useState({
    descricao: '',
    limite_requisicoes: 100,
    janela_tempo: 60
  })

  useEffect(() => {
    carregarKeys()
  }, [])

  const carregarKeys = async () => {
    try {
      setLoading(true)
      const res = await request('/api/keys/?apenas_ativas=false', { method: 'GET' })
      if (res.ok) {
        const data = await res.json()
        setKeys(Array.isArray(data) ? data : [])
      }
    } catch (error) {
      console.error('Erro ao carregar API Keys:', error)
      toast.error('Erro', 'Falha ao conectar com o servidor')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (e) => {
    e.preventDefault()
    try {
      // Pequeno feedback de loading no botão seria bom, mas mantendo simples
      const res = await request('/api/keys/', {
        method: 'POST',
        body: JSON.stringify(form)
      })
      
      if (res.ok) {
        const data = await res.json()
        setNewKeyData(data)
        setShowCreateModal(false)
        setShowSuccessModal(true)
        setForm({ descricao: '', limite_requisicoes: 100, janela_tempo: 60 })
        carregarKeys()
      } else {
        const err = await res.json()
        toast.error('Erro', err.detail || 'Falha ao criar chave')
      }
    } catch (error) {
      toast.error('Erro', 'Erro ao processar requisição')
    }
  }

  const toggleStatus = async (keyId, currentStatus) => {
    try {
      const res = await request(`/api/keys/${keyId}`, {
        method: 'PUT',
        body: JSON.stringify({ ativo: !currentStatus })
      })
      
      if (res.ok) {
        toast.success(
          !currentStatus ? 'Chave Ativada' : 'Chave Desativada', 
          `A chave foi ${!currentStatus ? 'habilitada' : 'suspensa'} com sucesso.`
        )
      } else {
        let errorMsg = 'Não foi possível alterar o status.'
        try {
          const errorData = await res.json()
          errorMsg = errorData?.detail || errorData?.message || errorMsg
        } catch (e) {}
        toast.error('Erro na Operação', errorMsg)
      }
    } catch (error) {
      console.error('Erro status:', error)
      toast.error('Erro de Processamento', error.message || 'Falha ao processar solicitação.')
    } finally {
      carregarKeys()
    }
  }

  const revokeKey = async (keyId) => {
    if (!window.confirm('CUIDADO: Revogar uma chave é uma ação permanente e interromperá qualquer sistema que a utilize. Continuar?')) return
    
    try {
      const res = await request(`/api/keys/${keyId}`, { method: 'DELETE' })
      
      if (res.ok) {
        toast.success('Chave Revogada', 'A chave foi removida do sistema com sucesso.')
      } else {
        let errorMsg = 'Não foi possível remover a chave.'
        try {
          const errorData = await res.json()
          errorMsg = errorData?.detail || errorData?.message || errorMsg
        } catch (e) {}
        toast.error('Erro ao Revogar', errorMsg)
      }
    } catch (error) {
      console.error('Erro revogar:', error)
      toast.error('Erro de Processamento', error.message || 'Falha ao concluir exclusão.')
    } finally {
      carregarKeys()
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    setIsCopying(true)
    toast.success('Copiado!', 'Chave copiada com sucesso.')
    setTimeout(() => setIsCopying(false), 2000)
  }

  const columns = [
    { 
      key: 'descricao', 
      label: 'Identificação & Prefixo', 
      render: (v, r) => (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          <span style={{ fontWeight: 600, fontSize: '0.95rem', color: 'var(--color-text-primary)' }}>{v}</span>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ 
              fontSize: '0.75rem', 
              fontFamily: 'monospace', 
              color: 'var(--color-primary)', 
              background: 'rgba(239, 68, 68, 0.1)',
              padding: '2px 6px',
              borderRadius: '4px'
            }}>
              {r.chave}
            </span>
          </div>
        </div>
      )
    },
    { 
      key: 'criado_em', 
      label: 'Data de Emissão', 
      width: 140,
      render: v => (
        <span style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>
          {new Date(v).toLocaleDateString('pt-BR')}
        </span>
      )
    },
    { 
      key: 'ultima_uso', 
      label: 'Última Atividade', 
      width: 180,
      render: v => (
        <span style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>
          {v ? new Date(v).toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' }) : 'Nunca utilizada'}
        </span>
      )
    },
    { 
      key: 'ativo', 
      label: 'Status da Chave', 
      width: 130,
      render: v => (
        v ? <Badge variant="success" dot>Habilitada</Badge> : <Badge variant="danger" dot>Suspensa</Badge>
      )
    }
  ]

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Chaves de API</h1>
          <p className="page-subtitle">Gerencie as credenciais de acesso para integradores, delivery e parceiros externos.</p>
        </div>
        <Button 
          variant="primary" 
          onClick={() => setShowCreateModal(true)}
          style={{ 
            boxShadow: '0 4px 12px rgba(239, 68, 68, 0.2)',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          <span>✨</span> Gerar Nova Chave
        </Button>
      </div>

      <div className="card" style={{ padding: '0', overflow: 'hidden', border: '1px solid var(--color-border)' }}>
        <Table
          columns={columns}
          data={keys}
          loading={loading}
          emptyMessage="Nenhuma chave de API emitida até o momento."
          actions={(row) => (
            <div style={{ display: 'flex', gap: '8px' }}>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => toggleStatus(row.id, row.ativo)}
                style={{ color: row.ativo ? 'var(--color-text-muted)' : 'var(--color-success)' }}
              >
                {row.ativo ? 'Suspender' : 'Habilitar'}
              </Button>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => revokeKey(row.id)}
                style={{ color: 'var(--color-danger)' }}
              >
                Revogar
              </Button>
            </div>
          )}
        />
      </div>

      {/* Modal de Criação */}
      <Modal 
        open={showCreateModal} 
        onClose={() => setShowCreateModal(false)}
        title="Gerar Nova Credencial"
      >
        <form onSubmit={handleCreate}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', padding: '10px 0' }}>
            <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', marginBottom: '4px' }}>
              Defina um nome identificador para esta conexão.
            </p>
            
            <Input
              label="Identificador do Parceiro"
              placeholder="Ex: iFood App, Dashboard Logística..."
              value={form.descricao}
              onChange={e => setForm({...form, descricao: e.target.value})}
              required
              autoFocus
            />
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <Input
                label="Limite de Requisições"
                type="number"
                value={form.limite_requisicoes}
                onChange={e => setForm({...form, limite_requisicoes: parseInt(e.target.value)})}
                required
                helper="Máximo de chamadas por janela"
              />
              <Input
                label="Janela de Tempo (min)"
                type="number"
                value={form.janela_tempo}
                onChange={e => setForm({...form, janela_tempo: parseInt(e.target.value)})}
                required
                helper="Duração do limite"
              />
            </div>

            <div style={{ 
              background: 'rgba(52, 211, 153, 0.05)', 
              padding: '12px', 
              borderRadius: '8px', 
              border: '1px solid rgba(52, 211, 153, 0.2)',
              fontSize: '0.8rem',
              color: '#059669'
            }}>
              💡 <strong>Dica:</strong> Chaves suspensas podem ser reativadas depois, mas chaves revogadas são excluídas para sempre.
            </div>

            <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '8px' }}>
              <Button type="button" variant="ghost" onClick={() => setShowCreateModal(false)}>Cancelar</Button>
              <Button type="submit" variant="primary">✨ Criar Chave Agora</Button>
            </div>
          </div>
        </form>
      </Modal>

      {/* Modal de Sucesso com Estilo Premium */}
      <Modal
        open={showSuccessModal}
        onClose={() => setShowSuccessModal(false)}
        title="🔑 Sua Chave de API foi criada!"
        size="md"
      >
        <div style={{ textAlign: 'center', padding: '10px 0' }}>
          <div style={{ 
            width: '64px', 
            height: '64px', 
            background: 'var(--color-success)', 
            borderRadius: '50%', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            fontSize: '32px',
            margin: '0 auto 20px',
            boxShadow: '0 8px 16px rgba(16, 185, 129, 0.2)'
          }}>
            ✅
          </div>

          <h3 style={{ marginBottom: '8px', color: 'var(--color-text-primary)' }}>Parceiro: {newKeyData?.descricao}</h3>
          
          <p style={{ marginBottom: '24px', color: 'var(--color-text-muted)', fontSize: '0.9rem', lineHeight: '1.5' }}>
            ⚠️ <strong>SEGURANÇA CRÍTICA:</strong> Copie esta chave agora. Por motivos de segurança, ela <strong>não poderá ser exibida novamente</strong> após fechar esta janela.
          </p>
          
          <div style={{ 
            background: 'var(--color-bg-secondary)', 
            padding: '20px', 
            borderRadius: '12px', 
            fontFamily: '"Fira Code", monospace',
            fontSize: '1rem',
            wordBreak: 'break-all',
            border: '2px solid var(--color-border)',
            marginBottom: '24px',
            position: 'relative',
            color: 'var(--color-primary)',
            fontWeight: 600,
            letterSpacing: '0.5px'
          }}>
            {newKeyData?.chave}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <Button 
              variant="primary" 
              style={{ width: '100%', height: '48px', fontSize: '1rem' }} 
              onClick={() => copyToClipboard(newKeyData?.chave)}
            >
              {isCopying ? '✅ Copiado com Sucesso!' : '📋 Copiar para Área de Transferência'}
            </Button>
            <Button 
              variant="ghost" 
              style={{ width: '100%' }} 
              onClick={() => setShowSuccessModal(false)}
            >
              Eu já guardei a chave em local seguro
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
