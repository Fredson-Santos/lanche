import { useState, useCallback } from 'react'

/**
 * Generic hook for async API calls.
 * Returns { data, loading, error, execute }
 */
export function useApi(apiFn, { immediate = false, initialData = null } = {}) {
  const [data,    setData]    = useState(initialData)
  const [loading, setLoading] = useState(immediate)
  const [error,   setError]   = useState(null)

  const execute = useCallback(async (...args) => {
    setLoading(true)
    setError(null)
    try {
      const result = await apiFn(...args)
      setData(result.data ?? result)
      return result
    } catch (err) {
      const msg = err?.response?.data?.detail || err?.message || 'Erro desconhecido'
      setError(msg)
      throw err
    } finally {
      setLoading(false)
    }
  }, [apiFn])

  return { data, loading, error, execute, setData }
}
