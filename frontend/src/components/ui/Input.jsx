import React from 'react'

export function Input({
  label,
  error,
  helper,
  icon,
  className = '',
  ...props
}) {
  return (
    <div className={`form-group ${className}`}>
      {label && <label className="form-label">{label}</label>}
      <div className={icon ? 'form-input-icon' : ''}>
        {icon && <span className="input-icon">{icon}</span>}
        <input className="form-input" {...props} />
      </div>
      {error  && <span className="form-error">{error}</span>}
      {!error && helper && <span className="form-helper">{helper}</span>}
    </div>
  )
}
