import React, { useEffect, useState, useCallback } from 'react'
import { Table } from '../components/ui/Table'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Select } from '../components/ui/Select'
import { Modal } from '../components/ui/Modal'
import { Badge, ActiveBadge, RoleBadge } from '../components/ui/Badge'
import { toast } from '../hooks/useToast'
import { userService } from '../services/userService'

const EMPTY_FORM = { username: '', email: '', role: 'caixa', senha: '' }

export function UsuariosPage() {
  const [users, setUsers]   = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [search, setSearch] = useState('')
  const [modal, setModal]   = useState({ open: false, mode: 'create', data: null })

  const load = useCallback(async () => {
    setLoading(true)
    const resp = await userService.getAll()
    setUsers(resp.data)
    setLoading(false)
  }, [])

  useEffect(() => { load() }, [load])

  const filtered = users.filter(u =>
    !search ||
    u.username.toLowerCase().includes(search.toLowerCase()) ||
    u.email.toLowerCase().includes(search.toLowerCase())
  )

  const openCreate = () => setModal({ open: true, mode: 'create', data: { ...EMPTY_FORM } })
  const openEdit   = (row) => setModal({ open: true, mode: 'edit', data: { ...row, senha: '' } })
  const closeModal = () => setModal(m => ({ ...m, open: false }))

  const handleSave = async () => {
    const { mode, data } = modal
    if (!data.username || !data.email || !data.role) {
      toast.error('Campos inválidos', 'Preencha nome, email e role.')
      return
    }
    setSaving(true)
    try {
      if (mode === 'create') {
        if (!data.senha) { toast.error('Senha obrigatória'); setSaving(false); return }
        await userService.create(data)
        toast.success('Usuário criado!', `${data.username} adicionado.`)
      } else {
        await userService.update(data.id, { username: data.username, email: data.email, role: data.role })
        toast.success('Usuário atualizado!')
      }
      await load()
      closeModal()
    } catch { toast.error('Erro', 'Não foi possível salvar.') }
    finally { setSaving(false) }
  }

  const handleToggle = async (row) => {
    try {
      await userService.toggleAtivo(row.id)
      toast.success(row.ativo ? 'Usuário desativado' : 'Usuário ativado')
      await load()
    } catch { toast.error('Erro', 'Operação falhou.') }
  }

  const handleDelete = async (row) => {
    if (!confirm(`Excluir usuário "${row.username}"?`)) return
    try {
      await userService.remove(row.id)
      toast.success('Usuário removido!')
      await load()
    } catch { toast.error('Erro', 'Não foi possível remover.') }
  }

  const columns = [
    { key: 'username', label: 'Nome',   render: (v, r) => (
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <div style={{ width: 32, height: 32, borderRadius: '50%', background: 'linear-gradient(135deg, var(--color-primary), #FB923C)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '0.78rem', color: 'white', flexShrink: 0 }}>
          {v.slice(0, 2).toUpperCase()}
        </div>
        <div>
          <div style={{ fontWeight: 600 }}>{v}</div>
          <div style={{ fontSize: '0.78rem', color: 'var(--color-text-muted)' }}>{r.email}</div>
        </div>
      </div>
    )},
    { key: 'role',    label: 'Role',   render: v => <RoleBadge role={v} />,  width: 110 },
    { key: 'ativo',   label: 'Status', render: v => <ActiveBadge value={v}/>, width: 100 },
    { key: 'data_criacao', label: 'Criado', render: v => v, width: 120 },
  ]

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Usuários</h1>
          <p className="page-subtitle">{users.length} usuário{users.length !== 1 ? 's' : ''} cadastrado{users.length !== 1 ? 's' : ''}</p>
        </div>
        <Button id="btn-novo-usuario" variant="primary" onClick={openCreate} icon="➕">
          Novo Usuário
        </Button>
      </div>

      {/* Search */}
      <div className="search-bar" style={{ marginBottom: '24px' }}>
        <div className="search-input-wrap">
          <span className="search-icon">🔍</span>
          <input
            id="usuario-search"
            className="form-input"
            placeholder="Buscar por nome ou email..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{ paddingLeft: '40px' }}
          />
        </div>
      </div>

      <Table
        columns={columns}
        data={filtered}
        loading={loading}
        emptyMessage="Nenhum usuário encontrado."
        actions={(row) => (
          <>
            <Button id={`btn-edit-user-${row.id}`} variant="ghost" size="sm" onClick={() => openEdit(row)}>✏️</Button>
            <Button
              id={`btn-toggle-user-${row.id}`}
              variant={row.ativo ? 'warning' : 'success'}
              size="sm"
              onClick={() => handleToggle(row)}
            >
              {row.ativo ? '🔇' : '✅'}
            </Button>
            <Button id={`btn-del-user-${row.id}`} variant="danger" size="sm" onClick={() => handleDelete(row)}>🗑️</Button>
          </>
        )}
      />

      {/* Modal */}
      <Modal
        open={modal.open}
        onClose={closeModal}
        title={modal.mode === 'create' ? '👤 Novo Usuário' : '✏️ Editar Usuário'}
        footer={
          <>
            <Button variant="ghost" onClick={closeModal}>Cancelar</Button>
            <Button variant="primary" onClick={handleSave} loading={saving}>Salvar</Button>
          </>
        }
      >
        <Input
          id="modal-user-nome"
          label="Nome de Usuário *"
          placeholder="Ex: João Silva"
          value={modal.data?.username ?? ''}
          onChange={e => setModal(m => ({ ...m, data: { ...m.data, username: e.target.value } }))}
        />
        <Input
          id="modal-user-email"
          label="E-mail *"
          type="email"
          placeholder="joao@lanche.com"
          value={modal.data?.email ?? ''}
          onChange={e => setModal(m => ({ ...m, data: { ...m.data, email: e.target.value } }))}
        />
        <Select
          id="modal-user-role"
          label="Role *"
          value={modal.data?.role ?? 'caixa'}
          onChange={e => setModal(m => ({ ...m, data: { ...m.data, role: e.target.value } }))}
        >
          <option value="caixa">Caixa</option>
          <option value="gerente">Gerente</option>
          <option value="admin">Admin</option>
        </Select>
        {modal.mode === 'create' && (
          <Input
            id="modal-user-senha"
            label="Senha *"
            type="password"
            placeholder="Mínimo 6 caracteres"
            value={modal.data?.senha ?? ''}
            onChange={e => setModal(m => ({ ...m, data: { ...m.data, senha: e.target.value } }))}
          />
        )}
      </Modal>
    </div>
  )
}
