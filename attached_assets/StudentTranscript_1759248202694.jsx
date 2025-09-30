import React, { useState, useEffect } from 'react'
import { supabase } from '../lib/supabaseClient.js'
import jsPDF from 'jspdf'

export default function StudentTranscript(){
  const [artifacts, setArtifacts] = useState([])
  const [user, setUser] = useState(null)

  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => {
      setUser(data.user)
      if (data.user) loadArtifacts(data.user.id)
    })
  }, [])

  async function loadArtifacts(studentId){
    const { data } = await supabase
      .from('artifacts_view')
      .select('*')
      .eq('student_id', studentId)
    setArtifacts(data || [])
  }

  function exportPDF(){
    const doc = new jsPDF()
    doc.setFontSize(14)
    doc.text('ODYC Skills Transcript', 14, 20)
    doc.setFontSize(11)
    doc.text(`Student: ${user?.email || ''}`, 14, 28)
    let y = 36
    artifacts.forEach(a => {
      const lines = doc.splitTextToSize(`• ${a.project_title} — ${a.badges || ''} — ${a.signed_off ? 'Signed' : 'Pending'}`, 180)
      doc.text(lines, 14, y)
      y += lines.length * 6 + 2
    })
    doc.save('ODYC_Skills_Transcript.pdf')
  }

  return (
    <div>
      <h2>Student Transcript</h2>
      <p>Artifacts and badges earned through mentor projects.</p>
      <button onClick={exportPDF}>Export PDF</button>
      <ul>
        {artifacts.map(a => (
          <li key={a.id}>{a.project_title} — {a.badges || ''} — {a.signed_off ? 'Signed' : 'Pending'}</li>
        ))}
      </ul>
    </div>
  )
}
