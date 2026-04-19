import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { ProtectedRoute } from './components/auth/ProtectedRoute'
import { ToastContainer } from './components/ui/Toast'

import { LoginPage }     from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'
import { VendasPage }    from './pages/VendasPage'
import { ProdutosPage }  from './pages/ProdutosPage'
import { EstoquePage }   from './pages/EstoquePage'
import { RelatoriosPage } from './pages/RelatoriosPage'
import { UsuariosPage }  from './pages/UsuariosPage'

import './styles/index.css'

function App() {
  return (
    <>
      <Routes>
        {/* Public */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />

        {/* Protected — all authenticated users */}
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/vendas"    element={<VendasPage />} />
          <Route path="/produtos"  element={<ProdutosPage />} />
          <Route path="/estoque"   element={<EstoquePage />} />
        </Route>

        {/* Protected — Gerente and Admin */}
        <Route element={<ProtectedRoute roles={['admin', 'gerente']} />}>
          <Route path="/relatorios" element={<RelatoriosPage />} />
        </Route>

        {/* Protected — Admin only */}
        <Route element={<ProtectedRoute roles={['admin']} />}>
          <Route path="/usuarios" element={<UsuariosPage />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>

      <ToastContainer />
    </>
  )
}

export default App
