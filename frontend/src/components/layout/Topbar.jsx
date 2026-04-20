import React, { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { RoleBadge } from '../ui/Badge'
import { Button } from '../ui/Button'

const PAGE_TITLES = {
  '/dashboard':  { title: 'Dashboard',  crumb: 'Visão geral do sistema' },
  '/vendas':     { title: 'Vendas',      crumb: 'Nova venda e histórico' },
  '/produtos':   { title: 'Produtos',    crumb: 'Gerenciamento de produtos' },
  '/estoque':    { title: 'Estoque',     crumb: 'Controle de estoque' },
  '/relatorios': { title: 'Relatórios',  crumb: 'Análise de vendas' },
  '/usuarios':   { title: 'Usuários',    crumb: 'Gerenciar usuários do sistema' },
}

export function Topbar() {
  const { user, logout } = useAuth()
  const { pathname } = useLocation()
  const navigate = useNavigate()
  const [showPopup, setShowPopup] = useState(false)
  const pageInfo = PAGE_TITLES[pathname] ?? { title: 'LANCHE', crumb: '' }
  const initials = user?.username?.slice(0, 2).toUpperCase() ?? 'LN'

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="topbar">
      <div className="topbar-left">
        <span className="topbar-page-title">{pageInfo.title}</span>
        {pageInfo.crumb && <span className="topbar-breadcrumb">{pageInfo.crumb}</span>}
      </div>
      {user && (
        <div className="topbar-right">
          <RoleBadge role={user.role} />
          <div 
            className="topbar-user" 
            style={{ position: 'relative', cursor: 'pointer' }}
            onClick={() => setShowPopup(!showPopup)}
          >
            <div className="topbar-avatar">{initials}</div>
            <div className="topbar-user-info">
              <span className="topbar-user-name">{user.username}</span>
              <span className="topbar-user-role">{user.email}</span>
            </div>

            {showPopup && (
              <div 
                className="animate-fade-in"
                style={{
                  position: 'absolute',
                  top: '120%',
                  right: 0,
                  background: 'var(--color-surface)',
                  border: '1px solid var(--color-border)',
                  borderRadius: '8px',
                  padding: '8px',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.5)',
                  zIndex: 50,
                  minWidth: '120px'
                }}
              >
                <Button variant="ghost" className="w-full" onClick={handleLogout}>
                  🚪 Sair
                </Button>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  )
}
