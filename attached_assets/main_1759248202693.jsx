import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import App from './App.jsx'
import Login from './pages/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import PathwayBuilder from './pages/PathwayBuilder.jsx'
import ProjectCardForm from './pages/ProjectCardForm.jsx'
import RubricBuilder from './pages/RubricBuilder.jsx'
import StudentTranscript from './pages/StudentTranscript.jsx'

const root = createRoot(document.getElementById('root'))
root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />}>
        <Route index element={<Navigate to="/login" />} />
        <Route path="login" element={<Login />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="pathways" element={<PathwayBuilder />} />
        <Route path="projects" element={<ProjectCardForm />} />
        <Route path="rubrics" element={<RubricBuilder />} />
        <Route path="transcript" element={<StudentTranscript />} />
      </Route>
    </Routes>
  </BrowserRouter>
)
