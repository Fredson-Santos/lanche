import React from 'react'

export function Button({
  children,
  variant = 'primary',
  size = '',
  className = '',
  loading = false,
  icon = null,
  iconOnly = false,
  ...props
}) {
  const cls = [
    'btn',
    `btn-${variant}`,
    size ? `btn-${size}` : '',
    iconOnly ? 'btn-icon' : '',
    className,
  ].filter(Boolean).join(' ')

  return (
    <button className={cls} disabled={loading || props.disabled} {...props}>
      {loading
        ? <span className="spinner spinner-sm" />
        : icon && <span>{icon}</span>
      }
      {!iconOnly && children}
    </button>
  )
}
