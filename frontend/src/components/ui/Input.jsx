import React from 'react'

export function Input({
  label,
  error,
  helper,
  icon,
  suffix,
  className = '',
  ...props
}) {
  return (
    <div className={`form-group ${className}`}>
      {label && <label className="form-label">{label}</label>}
      <div className={`input-wrapper ${icon ? 'form-input-icon' : ''}`}>
        {icon && <span className="input-icon">{icon}</span>}
        <input 
          className={`form-input ${suffix ? 'has-suffix' : ''}`} 
          {...props} 
        />
        {suffix && <div className="input-suffix">{suffix}</div>}
      </div>
      {error  && <span className="form-error">{error}</span>}
      {!error && helper && <span className="form-helper">{helper}</span>}
    </div>
  )
}

