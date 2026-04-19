import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { authService } from '../services/authService'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser]       = useState(null)
  const [token, setToken]     = useState(null)
  const [loading, setLoading] = useState(true)

  // Restore session from localStorage on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('lanche_token')
    const savedUser  = localStorage.getItem('lanche_user')
    if (savedToken && savedUser) {
      try {
        setToken(savedToken)
        setUser(JSON.parse(savedUser))
      } catch {
        localStorage.clear()
      }
    }
    setLoading(false)
  }, [])

  const login = useCallback(async (email, senha) => {
    const response = await authService.login(email, senha)
    const { access_token, user: userData } = response

    localStorage.setItem('lanche_token', access_token)
    localStorage.setItem('lanche_user', JSON.stringify(userData))

    setToken(access_token)
    setUser(userData)
    return userData
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('lanche_token')
    localStorage.removeItem('lanche_user')
    setToken(null)
    setUser(null)
  }, [])

  const isAuthenticated = Boolean(token && user)

  const hasRole = useCallback((...roles) => {
    if (!user) return false
    return roles.includes(user.role)
  }, [user])

  const value = {
    user,
    token,
    loading,
    isAuthenticated,
    login,
    logout,
    hasRole,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>')
  return ctx
}
