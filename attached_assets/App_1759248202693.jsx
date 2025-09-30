import React from 'react'
import { Outlet } from 'react-router-dom'
import NavBar from './components/NavBar.jsx'

export default function App() {
  return (
    <div style={{fontFamily: 'system-ui, -apple-system, Segoe UI, Roboto, sans-serif'}}>
      <NavBar />
      <div style={{maxWidth: 1000, margin: '20px auto', padding: 16}}>
        <Outlet />
      </div>
    </div>
  )
}
