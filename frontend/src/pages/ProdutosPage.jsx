import React, { useEffect, useState, useCallback } from 'react'
import { useAuth } from '../context/AuthContext'
import { Table } from '../components/ui/Table'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Select } from '../components/ui/Select'
import { Modal } from '../components/ui/Modal'
import { Badge, ActiveBadge } from '../components/ui/Badge'
import { toast } from '../hooks/useToast'
import { productService } from '../services/productService'

const fmtBRL = (v) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
const EMPTY_FORM = { nome: '', descricao: '', preco: '' }

export function ProdutosPage() {
  const { hasRole } = useAuth()
  const canManage = hasRole('admin', 'gerente')
  const canDelete = hasRole('admin')

  const [products, setProducts] = useState([])
  const [filtered, setFiltered] = useState([])
  const [loading, setLoading]   = useState(true)
  const [search, setSearch]     = useState('')
  const [filterAux, setFilter]  = useState('all') // all | ativo | inativo
  const [saving, setSaving]     = useState(false)

  const [modal, setModal] = useState({ open: false, mode: 'create', data: null })

  const load = useCallback(async () => {
    setLoading(true)
    const resp = await productService.getAll()
    setProducts(resp.data)
    setLoading(false)
  }, [])

  useEffect(() => { load() }, [load])

  useEffect(() => {
    let list = [...products]
    if (filterAux === 'ativo')   list = list.filter(p => p.ativo)
    if (filterAux === 'inativo') list = list.filter(p => !p.ativo)
    if (search) {
      const q = search.toLowerCase()
      list = list.filter(p => p.nome.toLowerCase().includes(q) || (p.descricao ?? '').toLowerCase().includes(q))
    }
    setFiltered(list)
  }, [products, search, filterAux])

  const openCreate = () => setModal({ open: true, mode: 'create', data: EMPTY_FORM })
  const openEdit   = (row) => setModal({ open: true, mode: 'edit', data: { ...row, preco: String(row.preco) } })
  const closeModal = () => setModal(m => ({ ...m, open: false }))

  const handleSave = async () => {
    const { mode, data } = modal
    if (!data.nome || !data.preco) { toast.error('Campos inválidos', 'Nome e preço são obrigatórios.'); return }
    setSaving(true)
    try {
      const payload = { nome: data.nome, descricao: data.descricao, preco: parseFloat(data.preco) }
      if (mode === 'create') {
        await productService.create(payload)
        toast.success('Produto criado!', `"${data.nome}" adicionado com sucesso.`)
      } else {
        await productService.update(data.id, payload)
        toast.success('Produto atualizado!')
      }
      await load()
      closeModal()
    } catch {
      toast.error('Erro', 'Não foi possível salvar o produto.')
    } finally {
      setSaving(false)
    }
  }

  const handleToggle = async (row) => {
    try {
      await productService.toggleAtivo(row.id)
      toast.success(row.ativo ? 'Produto desativado' : 'Produto ativado')
      await load()
    } catch { toast.error('Erro', 'Não foi possível alterar o status.') }
  }

  const handleDelete = async (row) => {
    if (!confirm(`Excluir "${row.nome}" permanentemente?`)) return
    try {
      await productService.remove(row.id)
      toast.success('Produto excluído!')
      await load()
    } catch { toast.error('Erro', 'Não foi possível excluir.') }
  }

  const columns = [
    { key: 'nome',     label: 'Nome',     render: (v, r) => (
      <div>
        <div style={{ fontWeight: 600 }}>{v}</div>
        {r.descricao && <div style={{ fontSize: '0.78rem', color: 'var(--color-text-muted)' }}>{r.descricao}</div>}
      </div>
    )},
    { key: 'preco',    label: 'Preço',    render: v => <span style={{ fontWeight: 600, color: 'var(--color-success)' }}>{fmtBRL(v)}</span> },
    { key: 'ativo',    label: 'Status',   render: v => <ActiveBadge value={v} />, width: 100 },
    { key: 'data_criacao', label: 'Criado em', render: v => v, width: 120 },
  ]

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Produtos</h1>
          <p className="page-subtitle">{filtered.length} produto{filtered.length !== 1 ? 's' : ''} encontrado{filtered.length !== 1 ? 's' : ''}</p>
        </div>
        {canManage && (
          <Button id="btn-novo-produto" variant="primary" onClick={openCreate} icon="➕">
            Novo Produto
          </Button>
        )}
      </div>

      {/* Filters */}
      <div className="search-bar" style={{ marginBottom: '24px' }}>
        <div className="search-input-wrap">
          <span className="search-icon">🔍</span>
          <input
            id="produto-search"
            className="form-input"
            placeholder="Buscar por nome ou descrição..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{ paddingLeft: '40px' }}
          />
        </div>
        <select
          id="produto-filter"
          className="form-select"
          value={filterAux}
          onChange={e => setFilter(e.target.value)}
          style={{ width: 'auto', minWidth: 140 }}
        >
          <option value="all">Todos</option>
          <option value="ativo">Ativos</option>
          <option value="inativo">Inativos</option>
        </select>
      </div>

      <Table
        columns={columns}
        data={filtered}
        loading={loading}
        emptyMessage="Nenhum produto encontrado."
        actions={canManage ? (row) => (
          <>
            <Button id={`btn-edit-produto-${row.id}`} variant="ghost" size="sm" onClick={() => openEdit(row)}>✏️</Button>
            <Button
              id={`btn-toggle-produto-${row.id}`}
              variant={row.ativo ? 'warning' : 'success'}
              size="sm"
              onClick={() => handleToggle(row)}
            >
              {row.ativo ? '🔇' : '✅'}
            </Button>
            {canDelete && (
              <Button id={`btn-del-produto-${row.id}`} variant="danger" size="sm" onClick={() => handleDelete(row)}>🗑️</Button>
            )}
          </>
        ) : null}
      />

      {/* Modal */}
      <Modal
        open={modal.open}
        onClose={closeModal}
        title={modal.mode === 'create' ? '➕ Novo Produto' : '✏️ Editar Produto'}
        footer={
          <>
            <Button variant="ghost" onClick={closeModal}>Cancelar</Button>
            <Button variant="primary" onClick={handleSave} loading={saving}>Salvar</Button>
          </>
        }
      >
        <Input
          id="modal-produto-nome"
          label="Nome do Produto *"
          placeholder="Ex: X-Burguer"
          value={modal.data?.nome ?? ''}
          onChange={e => setModal(m => ({ ...m, data: { ...m.data, nome: e.target.value } }))}
        />
        <Input
          id="modal-produto-descricao"
          label="Descrição"
          placeholder="Ingredientes ou detalhes"
          value={modal.data?.descricao ?? ''}
          onChange={e => setModal(m => ({ ...m, data: { ...m.data, descricao: e.target.value } }))}
        />
        <Input
          id="modal-produto-preco"
          label="Preço (R$) *"
          type="number"
          step="0.01"
          min="0.01"
          placeholder="0,00"
          value={modal.data?.preco ?? ''}
          onChange={e => setModal(m => ({ ...m, data: { ...m.data, preco: e.target.value } }))}
        />
      </Modal>
    </div>
  )
}
