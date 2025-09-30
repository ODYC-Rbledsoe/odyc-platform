import React, { useState } from 'react'
import { supabase } from '../lib/supabaseClient.js'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const [email, setEmail] = useState('')
  const [msg, setMsg] = useState('')
  const nav = useNavigate()

  async function signInWithEmail(e) {
    e.preventDefault()
    const { error } = await supabase.auth.signInWithOtp({ email })
    setMsg(error ? error.message : 'Check your email for the magic link.')
  }

  async function signInWithGoogle() {
    const { error } = await supabase.auth.signInWithOAuth({ provider: 'google' })
    if (error) alert(error.message)
  }

  supabase.auth.onAuthStateChange((event, session) => {
    if (session) nav('/dashboard')
  })

  return (
    <div>
      <h2>Sign in</h2>
      <button onClick={signInWithGoogle}>Continue with Google</button>
      <div style={{margin:'12px 0'}}>or</div>
      <form onSubmit={signInWithEmail}>
        <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="your@email.com" />
        <button type="submit">Send Magic Link</button>
      </form>
      <p>{msg}</p>
    </div>
  )
}
