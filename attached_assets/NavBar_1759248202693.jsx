import React from 'react'
import { Link } from 'react-router-dom'

export default function NavBar() {
  const nav = {display:'flex', gap:12, padding:'12px 16px', borderBottom:'1px solid #eee'}
  return (
    <div style={nav}>
      <Link to="/dashboard">Dashboard</Link>
      <Link to="/pathways">Pathway Builder</Link>
      <Link to="/projects">Project Cards</Link>
      <Link to="/rubrics">Rubrics</Link>
      <Link to="/transcript">Transcript</Link>
      <Link to="/login" style={{marginLeft:'auto'}}>Login</Link>
    </div>
  )
}
