import React from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { Button } from '../ui/Button'

const NAV_ITEMS = [
  { to: '/dashboard',  label: 'Dashboard',  icon: '📊', roles: ['admin', 'gerente', 'caixa'] },
  { to: '/vendas',     label: 'Vendas',      icon: '🛒', roles: ['admin', 'gerente', 'caixa'] },
  { to: '/produtos',   label: 'Produtos',    icon: '🍔', roles: ['admin', 'gerente', 'caixa'] },
  { to: '/estoque',    label: 'Estoque',     icon: '📦', roles: ['admin', 'gerente', 'caixa'] },
  { to: '/alertas',    label: 'Alertas',     icon: '⚠️', roles: ['admin', 'gerente'] },
  { to: '/reposicao',  label: 'Reposição',   icon: '🔄', roles: ['admin', 'gerente'] },
  { to: '/relatorios', label: 'Relatórios',  icon: '📈', roles: ['admin', 'gerente'] },
  { to: '/integracoes', label: 'Chaves de API', icon: '🔌', roles: ['admin'] },
  { to: '/usuarios',   label: 'Usuários',    icon: '👥', roles: ['admin'] },
]

export function Sidebar() {
  const { user, logout, hasRole } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const visibleItems = NAV_ITEMS.filter(item => hasRole(...item.roles))

  return (
    <aside className="sidebar" id="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">🍔</div>
        <div>
          <div className="sidebar-logo-text">LANCHE</div>
          <div className="sidebar-logo-sub">MVP Sistema</div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        <div className="sidebar-section-label">Menu</div>
        {visibleItems.map(item => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => `sidebar-item ${isActive ? 'active' : ''}`}
          >
            <span className="sidebar-item-icon">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="sidebar-footer">
        {user && (
          <div style={{ marginBottom: '12px', padding: '8px 12px', borderRadius: '8px', background: 'rgba(255,255,255,0.04)' }}>
            <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--color-text-primary)' }}>
              {user.username}
            </div>
            <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)' }}>
              {user.email}
            </div>
          </div>
        )}
        <Button variant="ghost" className="w-full" onClick={handleLogout}>
          🚪 Sair
        </Button>
      </div>
    </aside>
  )
}
