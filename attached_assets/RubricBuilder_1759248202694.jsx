import React, { useState, useEffect } from 'react'
import { supabase } from '../lib/supabaseClient.js'

export default function RubricBuilder(){
  const [pathways, setPathways] = useState([])
  const [pathwayId, setPathwayId] = useState(null)
  const [competency, setCompetency] = useState('Lockout/Tagout')
  const [novice, setNovice] = useState('Identifies energy sources with guidance.')
  const [developing, setDeveloping] = useState('Performs LOTO with minor prompts; completes checklist.')
  const [proficient, setProficient] = useState('Executes LOTO end-to-end; verifies try-out; completes documentation independently.')
  const [message, setMessage] = useState('')

  useEffect(() => {
    supabase.from('pathways').select('id,title').then(({data}) => setPathways(data||[]))
  }, [])

  async function saveRubric(){
    const payload = { pathway_id: pathwayId, competency, novice, developing, proficient }
    const { error } = await supabase.from('rubrics').insert(payload)
    setMessage(error ? error.message : 'Rubric row saved.')
  }

  return (
    <div>
      <h2>Rubric Builder</h2>
      <label>Pathway</label><br/>
      <select onChange={e=>setPathwayId(e.target.value)}>
        <option>Select a pathway</option>
        {pathways.map(p=> <option key={p.id} value={p.id}>{p.title}</option>)}
      </select><br/><br/>
      <label>Competency</label><br/>
      <input value={competency} onChange={e=>setCompetency(e.target.value)} style={{width:'100%'}}/><br/><br/>
      <label>Novice</label><br/>
      <textarea value={novice} onChange={e=>setNovice(e.target.value)} style={{width:'100%'}}/><br/><br/>
      <label>Developing</label><br/>
      <textarea value={developing} onChange={e=>setDeveloping(e.target.value)} style={{width:'100%'}}/><br/><br/>
      <label>Proficient</label><br/>
      <textarea value={proficient} onChange={e=>setProficient(e.target.value)} style={{width:'100%'}}/><br/><br/>
      <button onClick={saveRubric}>Save Rubric Row</button>
      <p>{message}</p>
    </div>
  )
}
