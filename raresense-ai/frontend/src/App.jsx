import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Patients from './pages/Patients'
import PatientDetail from './pages/PatientDetail'
import Diseases from './pages/Diseases'
import Search from './pages/Search'
import AIAssistant from './pages/AIAssistant'
import PatientDashboard from './pages/PatientDashboard'
import Login from './pages/Login'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('raresense_token')
    const savedUser = localStorage.getItem('raresense_user')
    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser))
      } catch {
        localStorage.removeItem('raresense_token')
        localStorage.removeItem('raresense_user')
      }
    }
    setLoading(false)
  }, [])

  const handleLogin = (userData, token) => {
    localStorage.setItem('raresense_token', token)
    localStorage.setItem('raresense_user', JSON.stringify(userData))
    setUser(userData)
  }

  const handleLogout = () => {
    localStorage.removeItem('raresense_token')
    localStorage.removeItem('raresense_user')
    setUser(null)
  }

  if (loading) {
    return (
      <div className="loading-container" style={{ minHeight: '100vh' }}>
        <div className="spinner" />
      </div>
    )
  }

  if (!user) {
    return <Login onLogin={handleLogin} />
  }

  if (user.role === 'patient') {
    return (
      <BrowserRouter>
        <Layout user={user} onLogout={handleLogout}>
          <Routes>
            <Route path="/patient-dashboard" element={<PatientDashboard />} />
            <Route path="*" element={<Navigate to="/patient-dashboard" replace />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    )
  }

  return (
    <BrowserRouter>
      <Layout user={user} onLogout={handleLogout}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/patients" element={<Patients />} />
          <Route path="/patients/:id" element={<PatientDetail user={user} />} />
          <Route path="/diseases" element={<Diseases />} />
          <Route path="/search" element={<Search />} />
          <Route path="/ai-assistant" element={<AIAssistant />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
