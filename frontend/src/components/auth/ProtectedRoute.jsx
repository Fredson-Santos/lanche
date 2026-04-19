import React from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { Layout } from '../layout/Layout'
import { Spinner } from '../ui/Spinner'

export function ProtectedRoute({ roles }) {
  const { isAuthenticated, loading, hasRole } = useAuth()

  if (loading) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
        <Spinner size="xl" />
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (roles && !hasRole(...roles)) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <Layout>
      <Outlet />
    </Layout>
  )
}
