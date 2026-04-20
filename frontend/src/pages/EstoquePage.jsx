import React, { useEffect, useState, useCallback } from 'react'
import { useAuth } from '../context/AuthContext'
import { Table } from '../components/ui/Table'
import { Button } from '../components/ui/Button'
import { Modal } from '../components/ui/Modal'
import { Input } from '../components/ui/Input'
import { Badge } from '../components/ui/Badge'
import { Spinner } from '../components/ui/Spinner'
import { toast } from '../hooks/useToast'
import { stockService } from '../services/stockService'

const LEVELS = (q) => {
  if (q === 0)  return { label: 'Sem estoque', variant: 'danger',  level: 'low',    pct: 0 }
  if (q < 10)   return { label: 'Crítico',     variant: 'danger',  level: 'low',    pct: Math.min((q / 10) * 33, 33) }
  if (q < 30)   return { label: 'Baixo',       variant: 'warning', level: 'medium', pct: 33 + Math.min(((q - 10) / 20) * 33, 33) }
  return         { label: 'Normal',            variant: 'success', level: 'high',   pct: 66 + Math.min(((q - 30) / 70) * 34, 34) }
}

export function EstoquePage() {
  const { hasRole } = useAuth()
  const canEdit = hasRole('admin', 'gerente')

  const [stock, setStock]   = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [saving, setSaving] = useState(false)
  const [modal, setModal]   = useState({ open: false, item: null, qty: '' })

  const load = useCallback(async () => {
    setLoading(true)
    const resp = await stockService.getAll()
    const mapped = resp.data.map(s => ({
      ...s,
      nome: s.produto?.nome || 'Sem nome'
    }))
    setStock(mapped)
    setLoading(false)
  }, [])

  useEffect(() => { load() }, [load])

  const filtered = stock.filter(s =>
    !search || s.nome.toLowerCase().includes(search.toLowerCase())
  )

  const openEdit = (item) => setModal({ open: true, item, qty: String(item.quantidade) })
  const closeModal = () => setModal(m => ({ ...m, open: false }))

  const handleSave = async () => {
    const qty = parseInt(modal.qty, 10)
    if (isNaN(qty) || qty < 0) { toast.error('Quantidade inválida', 'Digite um número ≥ 0.'); return }
    setSaving(true)
    try {
      await stockService.update(modal.item.id, qty)
      toast.success('Estoque atualizado!', `${modal.item.nome}: ${qty} unid.`)
      await load()
      closeModal()
    } catch { toast.error('Erro', 'Não foi possível atualizar.') }
    finally { setSaving(false) }
  }

  const columns = [
    { key: 'nome',       label: 'Produto',     render: v => <span style={{ fontWeight: 500 }}>{v}</span> },
    { key: 'quantidade', label: 'Qtd.',         render: v => <span style={{ fontWeight: 700 }}>{v}</span>, width: 80 },
    { key: 'status',     label: 'Status',       render: (v, r) => {
      const lvl = LEVELS(r.quantidade)
      return (
        <div className="stock-bar-wrap">
          <div className="stock-bar">
            <div className={`stock-bar-fill ${lvl.level}`} style={{ width: `${lvl.pct}%` }} />
          </div>
          <Badge variant={lvl.variant} dot>{lvl.label}</Badge>
        </div>
      )
    }},
  ]

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Estoque</h1>
          <p className="page-subtitle">Controle de quantidade por produto</p>
        </div>
      </div>

      {/* Search */}
      <div className="search-bar" style={{ marginBottom: '24px' }}>
        <div className="search-input-wrap">
          <span className="search-icon">🔍</span>
          <input
            id="estoque-search"
            className="form-input"
            placeholder="Buscar produto..."
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
        emptyMessage="Nenhum item de estoque encontrado."
        actions={canEdit ? (row) => (
          <Button
            id={`btn-edit-estoque-${row.id}`}
            variant="ghost"
            size="sm"
            onClick={() => openEdit(row)}
          >
            ✏️ Ajustar
          </Button>
        ) : null}
      />

      {/* Edit Modal */}
      <Modal
        open={modal.open}
        onClose={closeModal}
        title={`📦 Ajustar Estoque — ${modal.item?.nome}`}
        footer={
          <>
            <Button variant="ghost" onClick={closeModal}>Cancelar</Button>
            <Button variant="primary" onClick={handleSave} loading={saving}>Salvar</Button>
          </>
        }
      >
        <Input
          id="modal-estoque-qty"
          label="Nova Quantidade"
          type="number"
          min="0"
          value={modal.qty}
          onChange={e => setModal(m => ({ ...m, qty: e.target.value }))}
          helper="Digite a quantidade atual real em estoque."
        />
      </Modal>
    </div>
  )
}
