import React from 'react'

const variants = {
  success: 'badge-success',
  danger:  'badge-danger',
  warning: 'badge-warning',
  info:    'badge-info',
  primary: 'badge-primary',
  neutral: 'badge-neutral',
}

export function Badge({ children, variant = 'neutral', dot = false }) {
  return (
    <span className={`badge ${variants[variant] ?? 'badge-neutral'} ${dot ? 'badge-dot' : ''}`}>
      {children}
    </span>
  )
}

// Convenience for boolean active status
export function ActiveBadge({ value }) {
  return (
    <Badge variant={value ? 'success' : 'danger'} dot>
      {value ? 'Ativo' : 'Inativo'}
    </Badge>
  )
}

// Role badge
const ROLE_CONFIG = {
  admin:   { label: 'Admin',   variant: 'danger'  },
  gerente: { label: 'Gerente', variant: 'warning'  },
  caixa:   { label: 'Caixa',   variant: 'info'    },
}

export function RoleBadge({ role }) {
  const cfg = ROLE_CONFIG[role] ?? { label: role, variant: 'neutral' }
  return <Badge variant={cfg.variant}>{cfg.label}</Badge>
}
