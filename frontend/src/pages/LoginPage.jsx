import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Input } from '../components/ui/Input'
import { Button } from '../components/ui/Button'
import { toast } from '../hooks/useToast'

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()

  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [showSenha, setShowSenha] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!email || !senha) { setError('Preencha email e senha.'); return }
    setLoading(true)
    setError('')
    try {
      const user = await login(email, senha)
      toast.success(`Bem-vindo, ${user.username}!`)
      navigate('/dashboard')
    } catch (err) {
      const msg = err?.response?.data?.detail || 'Email ou senha incorretos.'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-bg-orb login-bg-orb-1" />
      <div className="login-bg-orb login-bg-orb-2" />

      <div className="login-card animate-slide-up">
        {/* Logo */}
        <div className="login-logo">
          <div className="login-logo-icon">🍔</div>
          <div className="login-logo-title">LANCHE MVP</div>
          <div className="login-logo-sub">Sistema de Gestão para Varejo Alimentício</div>
        </div>

        {/* Demo hints */}
        <div className="login-hint">
          <div className="login-hint-title">🔑 Credenciais de acesso</div>
          <div className="login-hint-item">👑 <strong>admin@lanche.com</strong> / admin123 — Admin</div>
          <div className="login-hint-item">📋 <strong>gerente@lanche.com</strong> / gerente123 — Gerente</div>
          <div className="login-hint-item">💳 <strong>caixa@lanche.com</strong> / caixa123 — Caixa</div>
        </div>

        {/* Form */}
        <form className="login-form" onSubmit={handleSubmit} id="login-form">
          <Input
            id="login-email"
            label="E-mail"
            type="email"
            placeholder="seu@email.com"
            value={email}
            onChange={e => setEmail(e.target.value)}
            icon="✉️"
            autoFocus
          />
          <Input
            id="login-senha"
            label="Senha"
            type={showSenha ? 'text' : 'password'}
            placeholder="••••••••"
            value={senha}
            onChange={e => setSenha(e.target.value)}
            icon="🔒"
            suffix={
              <button 
                type="button" 
                onClick={() => setShowSenha(!showSenha)}
                title={showSenha ? "Esconder senha" : "Ver senha"}
                style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0, display: 'flex', alignItems: 'center' }}
              >
                {showSenha ? '👁️‍G️' : '👁️'}
              </button>
            }
          />

          {error && (
            <div style={{
              background: 'var(--color-danger-bg)',
              border: '1px solid rgba(239,68,68,0.3)',
              borderRadius: 'var(--radius-md)',
              padding: '10px 14px',
              fontSize: '0.85rem',
              color: 'var(--color-danger)',
            }}>
              ⚠️ {error}
            </div>
          )}

          <Button
            id="login-submit"
            type="submit"
            variant="primary"
            size="lg"
            className="w-full"
            loading={loading}
          >
            Entrar no Sistema
          </Button>
        </form>
      </div>
    </div>
  )
}
