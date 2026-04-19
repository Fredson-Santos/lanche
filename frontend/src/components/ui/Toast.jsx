import React from 'react'
import { useToastProvider } from '../../hooks/useToast'

const ICONS = {
  success: '✅',
  danger:  '❌',
  warning: '⚠️',
  info:    'ℹ️',
}

export function ToastContainer() {
  const toasts = useToastProvider()

  return (
    <div className="toast-container">
      {toasts.map(t => (
        <div key={t.id} className={`toast toast-${t.type}`}>
          <span className="toast-icon">{ICONS[t.type]}</span>
          <div className="toast-content">
            <div className="toast-title">{t.title}</div>
            {t.message && <div className="toast-message">{t.message}</div>}
          </div>
        </div>
      ))}
    </div>
  )
}
