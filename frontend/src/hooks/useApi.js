import { useState, useCallback } from 'react'
import api from '../services/api'

/**
 * Generic hook for async API calls.
 * Returns { data, loading, error, execute, request }
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

  const request = useCallback(async (url, options = {}) => {
    try {
      let reqData = options.body;
      if (typeof options.body === 'string') {
        try { reqData = JSON.parse(options.body) } catch (e) {}
      }

      const response = await api({
        url,
        method: options.method || 'GET',
        data: reqData,
      });

      return {
        ok: response.status >= 200 && response.status < 300,
        status: response.status,
        json: async () => response.data,
      };
    } catch (err) {
      if (err.response) {
        return {
          ok: false,
          status: err.response.status,
          json: async () => err.response.data,
        };
      }
      throw err;
    }
  }, []);

  return { data, loading, error, execute, setData, request }
}
