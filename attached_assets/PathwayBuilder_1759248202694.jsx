import React, { useState } from 'react'
import { supabase } from '../lib/supabaseClient.js'

export default function PathwayBuilder(){
  const [title, setTitle] = useState('')
  const [ksas, setKsas] = useState('Tools; Safety; Troubleshooting')
  const [milestones, setMilestones] = useState('Entry; 6 months; 12 months; 24 months')
  const [wageBands, setWageBands] = useState('$20-24; $24-28; $28-34')
  const [message, setMessage] = useState('')

  async function savePathway(){
    const payload = {
      title,
      ksas: ksas.split(';').map(s=>s.trim()),
      milestones: milestones.split(';').map(s=>s.trim()),
      wage_bands: wageBands.split(';').map(s=>s.trim())
    }
    const { error } = await supabase.from('pathways').insert(payload)
    setMessage(error ? error.message : 'Pathway saved.')
    if(!error){ setTitle('') }
  }

  return (
    <div>
      <h2>Pathway Builder</h2>
      <label>Title</label><br/>
      <input value={title} onChange={e=>setTitle(e.target.value)} placeholder="Maintenance Technician" style={{width:'100%'}}/><br/><br/>
      <label>KSAs (semicolon separated)</label><br/>
      <input value={ksas} onChange={e=>setKsas(e.target.value)} style={{width:'100%'}}/><br/><br/>
      <label>Milestones (semicolon separated)</label><br/>
      <input value={milestones} onChange={e=>setMilestones(e.target.value)} style={{width:'100%'}}/><br/><br/>
      <label>Wage Bands (semicolon separated)</label><br/>
      <input value={wageBands} onChange={e=>setWageBands(e.target.value)} style={{width:'100%'}}/><br/><br/>
      <button onClick={savePathway}>Save Pathway</button>
      <p>{message}</p>
    </div>
  )
}
