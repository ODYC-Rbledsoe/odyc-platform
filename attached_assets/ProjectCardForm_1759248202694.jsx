import React, { useState, useEffect } from 'react'
import { supabase } from '../lib/supabaseClient.js'

export default function ProjectCardForm(){
  const [pathways, setPathways] = useState([])
  const [pathwayId, setPathwayId] = useState(null)
  const [title, setTitle] = useState('Lockout/Tagout Walkdown')
  const [duration, setDuration] = useState(4)
  const [objective, setObjective] = useState('Perform an LOTO walkdown on a pump circuit and document steps.')
  const [prereqs, setPrereqs] = useState('Site orientation; PPE')
  const [steps, setSteps] = useState('Identify energy sources; Verify procedures; Apply locks; Try-out; Remove locks')
  const [artifact, setArtifact] = useState('Checklist + photos')
  const [capacity, setCapacity] = useState(4)
  const [message, setMessage] = useState('')

  useEffect(() => {
    supabase.from('pathways').select('id,title').then(({data}) => setPathways(data||[]))
  }, [])

  async function saveProject(){
    const payload = {
      pathway_id: pathwayId,
      title,
      duration_hours: Number(duration),
      objective,
      prereqs: prereqs.split(';').map(s=>s.trim()),
      steps: steps.split(';').map(s=>s.trim()),
      artifact_spec: {type:'checklist+photos', notes:artifact},
      capacity_month: Number(capacity)
    }
    const { error } = await supabase.from('project_cards').insert(payload)
    setMessage(error ? error.message : 'Project card saved.')
  }

  return (
    <div>
      <h2>Project Card</h2>
      <label>Pathway</label><br/>
      <select onChange={e=>setPathwayId(e.target.value)}>
        <option>Select a pathway</option>
        {pathways.map(p=> <option key={p.id} value={p.id}>{p.title}</option>)}
      </select><br/><br/>
      <label>Title</label><br/>
      <input value={title} onChange={e=>setTitle(e.target.value)} style={{width:'100%'}}/><br/><br/>
      <label>Duration (hours)</label><br/>
      <input type="number" value={duration} onChange={e=>setDuration(e.target.value)} /><br/><br/>
      <label>Objective</label><br/>
      <textarea value={objective} onChange={e=>setObjective(e.target.value)} style={{width:'100%'}}/><br/><br/>
      <label>Prereqs (; separated)</label><br/>
      <input value={prereqs} onChange={e=>setPrereqs(e.target.value)} style={{width:'100%'}}/><br/><br/>
      <label>Steps (; separated)</label><br/>
      <input value={steps} onChange={e=>setSteps(e.target.value)} style={{width:'100%'}}/><br/><br/>
      <label>Artifact notes</label><br/>
      <input value={artifact} onChange={e=>setArtifact(e.target.value)} style={{width:'100%'}}/><br/><br/>
      <label>Capacity / month</label><br/>
      <input type="number" value={capacity} onChange={e=>setCapacity(e.target.value)} /><br/><br/>
      <button onClick={saveProject}>Save Project Card</button>
      <p>{message}</p>
    </div>
  )
}
