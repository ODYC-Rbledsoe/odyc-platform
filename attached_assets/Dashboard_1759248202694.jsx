import React, { useEffect, useState } from 'react'
import { supabase } from '../lib/supabaseClient.js'

export default function Dashboard(){
  const [user, setUser] = useState(null)
  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => setUser(data.user))
  }, [])
  return (
    <div>
      <h2>Dashboard</h2>
      {user ? <p>Signed in as {user.email}</p> : <p>Not signed in</p>}
      <ul>
        <li>Create a Pathway and add Project Cards</li>
        <li>Invite educators to map standards and publish projects</li>
        <li>Students complete projects and upload artifacts</li>
      </ul>
    </div>
  )
}
