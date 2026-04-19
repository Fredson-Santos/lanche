import { useState, useCallback } from 'react'

let _setToasts = null

export function useToastProvider() {
  const [toasts, setToasts] = useState([])
  _setToasts = setToasts
  return toasts
}

function addToast(type, title, message, duration = 3500) {
  if (!_setToasts) return
  const id = Date.now() + Math.random()
  _setToasts(prev => [...prev, { id, type, title, message }])
  setTimeout(() => {
    _setToasts(prev => prev.filter(t => t.id !== id))
  }, duration)
}

export const toast = {
  success: (title, message) => addToast('success', title, message),
  error:   (title, message) => addToast('danger',  title, message),
  warning: (title, message) => addToast('warning', title, message),
  info:    (title, message) => addToast('info',    title, message),
}

export function useToast() {
  return toast
}
