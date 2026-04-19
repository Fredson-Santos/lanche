import React from 'react'
import { Sidebar } from './Sidebar'
import { Topbar } from './Topbar'

export function Layout({ children }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <main className="app-main">
        <Topbar />
        <div className="app-content animate-fade-in">
          {children}
        </div>
      </main>
    </div>
  )
}
