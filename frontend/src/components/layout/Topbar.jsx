import React from 'react'
import { useLocation } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { RoleBadge } from '../ui/Badge'

const PAGE_TITLES = {
  '/dashboard':  { title: 'Dashboard',  crumb: 'Visão geral do sistema' },
  '/vendas':     { title: 'Vendas',      crumb: 'Nova venda e histórico' },
  '/produtos':   { title: 'Produtos',    crumb: 'Gerenciamento de produtos' },
  '/estoque':    { title: 'Estoque',     crumb: 'Controle de estoque' },
  '/relatorios': { title: 'Relatórios',  crumb: 'Análise de vendas' },
  '/usuarios':   { title: 'Usuários',    crumb: 'Gerenciar usuários do sistema' },
}

export function Topbar() {
  const { user } = useAuth()
  const { pathname } = useLocation()
  const pageInfo = PAGE_TITLES[pathname] ?? { title: 'LANCHE', crumb: '' }
  const initials = user?.username?.slice(0, 2).toUpperCase() ?? 'LN'

  return (
    <header className="topbar">
      <div className="topbar-left">
        <span className="topbar-page-title">{pageInfo.title}</span>
        {pageInfo.crumb && <span className="topbar-breadcrumb">{pageInfo.crumb}</span>}
      </div>
      {user && (
        <div className="topbar-right">
          <RoleBadge role={user.role} />
          <div className="topbar-user">
            <div className="topbar-avatar">{initials}</div>
            <div className="topbar-user-info">
              <span className="topbar-user-name">{user.username}</span>
              <span className="topbar-user-role">{user.email}</span>
            </div>
          </div>
        </div>
      )}
    </header>
  )
}
