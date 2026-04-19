import React from 'react'

export function StatCard({ label, value, icon, trend, trendLabel, accentColor }) {
  const style = accentColor ? { '--accent': accentColor } : {}

  return (
    <div className="stat-card" style={style}>
      <div className="stat-card-icon" style={accentColor ? { background: `${accentColor}18`, color: accentColor } : {}}>
        {icon}
      </div>
      <div>
        <div className="stat-card-value">{value}</div>
        <div className="stat-card-label">{label}</div>
      </div>
      {trend !== undefined && (
        <div className={`stat-card-trend ${trend >= 0 ? 'up' : 'down'}`}>
          {trend >= 0 ? '↑' : '↓'} {Math.abs(trend)}% {trendLabel}
        </div>
      )}
    </div>
  )
}
