import { useState } from 'react'
import { api } from '../utils/api'
import { LogIn, UserPlus } from 'lucide-react'

export default function Login({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false)
  const [form, setForm] = useState({ username: '', password: '', email: '', full_name: '', specialty: '', role: 'clinician' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      let result
      if (isRegister) {
        result = await api.register(form)
      } else {
        result = await api.login({ username: form.username, password: form.password })
      }
      onLogin(result.user, result.access_token)
    } catch (err) {
      setError(err.message || 'Authentication failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-card slide-up">
        <div className="logo">
          <div className="logo-icon">RS</div>
          <h2>RareSense.AI</h2>
          <p>LLM-Powered Rare Disease Detection</p>
        </div>

        {error && <div className="login-error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              className="form-input"
              type="text"
              placeholder="Enter username"
              value={form.username}
              onChange={e => setForm({ ...form, username: e.target.value })}
              required
            />
          </div>

          {isRegister && (
            <>
              <div className="form-group">
                <label>Full Name</label>
                <input
                  className="form-input"
                  type="text"
                  placeholder="Dr. John Smith"
                  value={form.full_name}
                  onChange={e => setForm({ ...form, full_name: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>Email</label>
                <input
                  className="form-input"
                  type="email"
                  placeholder="doctor@hospital.com"
                  value={form.email}
                  onChange={e => setForm({ ...form, email: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>Specialty</label>
                <input
                  className="form-input"
                  type="text"
                  placeholder="Rheumatology"
                  value={form.specialty}
                  onChange={e => setForm({ ...form, specialty: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label>Role</label>
                <select
                  className="form-input"
                  value={form.role}
                  onChange={e => setForm({ ...form, role: e.target.value })}
                >
                  <option value="clinician">Clinician</option>
                  <option value="patient">Patient</option>
                  <option value="researcher">Researcher</option>
                </select>
              </div>
            </>
          )}

          <div className="form-group">
            <label>Password</label>
            <input
              className="form-input"
              type="password"
              placeholder="Enter password"
              value={form.password}
              onChange={e => setForm({ ...form, password: e.target.value })}
              required
            />
          </div>

          <button
            className="btn btn-primary btn-lg"
            type="submit"
            disabled={loading}
            style={{ width: '100%', justifyContent: 'center', marginTop: '0.5rem' }}
          >
            {loading ? (
              <span className="loading-dots"><span></span><span></span><span></span></span>
            ) : isRegister ? (
              <><UserPlus size={18} /> Create Account</>
            ) : (
              <><LogIn size={18} /> Sign In</>
            )}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '1.25rem' }}>
          <button
            className="btn btn-secondary btn-sm"
            onClick={() => { setIsRegister(!isRegister); setError('') }}
            style={{ background: 'transparent', border: 'none', color: 'var(--accent-light)', fontSize: '0.8rem' }}
          >
            {isRegister ? 'Already have an account? Sign In' : "Don't have an account? Register"}
          </button>
        </div>

        {!isRegister && (
          <div style={{
            marginTop: '1.5rem',
            padding: '0.85rem',
            background: 'var(--bg-elevated)',
            borderRadius: 'var(--radius-sm)',
            fontSize: '0.75rem',
            color: 'var(--text-tertiary)'
          }}>
            <strong style={{ color: 'var(--text-secondary)' }}>Demo Credentials:</strong>
            <div style={{ marginTop: '0.35rem', display: 'grid', gap: '0.15rem' }}>
              <span>Admin: <code style={{ color: 'var(--accent-light)' }}>admin</code> / <code style={{ color: 'var(--accent-light)' }}>admin123</code></span>
              <span>Clinician: <code style={{ color: 'var(--accent-light)' }}>clinician</code> / <code style={{ color: 'var(--accent-light)' }}>clinician123</code></span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
