import React from 'react'
import { Spinner } from './Spinner'

export function Table({ columns, data, loading, emptyMessage = 'Nenhum registro encontrado', actions }) {
  return (
    <div className="table-container">
      <table className="table">
        <thead>
          <tr>
            {columns.map(col => (
              <th key={col.key} style={col.width ? { width: col.width } : {}}>
                {col.label}
              </th>
            ))}
            {actions && <th style={{ width: 120 }}>Ações</th>}
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={columns.length + (actions ? 1 : 0)}>
                <div className="loading-overlay">
                  <Spinner size="lg" />
                  <span>Carregando...</span>
                </div>
              </td>
            </tr>
          ) : data.length === 0 ? (
            <tr>
              <td colSpan={columns.length + (actions ? 1 : 0)}>
                <div className="empty-state" style={{ padding: '40px 24px' }}>
                  <div className="empty-state-icon">📭</div>
                  <p className="empty-state-title">{emptyMessage}</p>
                </div>
              </td>
            </tr>
          ) : (
            data.map((row, i) => (
              <tr key={row.id ?? i}>
                {columns.map(col => (
                  <td key={col.key}>
                    {col.render ? col.render(row[col.key], row) : row[col.key]}
                  </td>
                ))}
                {actions && (
                  <td>
                    <div className="table-actions">
                      {actions(row)}
                    </div>
                  </td>
                )}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}
