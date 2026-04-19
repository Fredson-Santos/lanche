import React from 'react'

export function Spinner({ size = '', color }) {
  return (
    <span
      className={`spinner ${size ? `spinner-${size}` : ''}`}
      style={color ? { borderTopColor: color } : {}}
    />
  )
}
