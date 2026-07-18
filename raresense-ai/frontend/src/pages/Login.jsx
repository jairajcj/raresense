import { useState, useEffect } from 'react'
import { api } from '../utils/api'
import { AlertCircle, RefreshCw, Shield, Mail, KeyRound, UserPlus } from 'lucide-react'

export default function Login({ onLogin }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [selectedRole, setSelectedRole] = useState('clinician')

  // ── Clinician state ──
  const [clinicianMode, setClinicianMode] = useState('code') // 'code' | 'otp'
  const [clinicianEmail, setClinicianEmail] = useState('')
  const [clinicianName, setClinicianName] = useState('')
  const [institutionalCode, setInstitutionalCode] = useState('')
  const [otpEmail, setOtpEmail] = useState('')
  const [otpCode, setOtpCode] = useState('')
  const [otpSent, setOtpSent] = useState(false)
  const [otpHint, setOtpHint] = useState('')

  // ── Patient state ──
  const [patientName, setPatientName] = useState('')
  const [patientEmail, setPatientEmail] = useState('')
  const [patientPassword, setPatientPassword] = useState('')
  const [patientMode, setPatientMode] = useState('google') // 'google' | 'register'

  // Generate 12 segments for the medical DNA helix
  const helixSegments = Array.from({ length: 12 })

  // Initialize Google Identity Services SDK (only for patient portal)
  useEffect(() => {
    if (selectedRole !== 'patient') return

    const initGoogleSDK = async () => {
      try {
        const config = await api.getGoogleConfig()
        const clientId = config.client_id || '503719948259-mockclientid.apps.googleusercontent.com'

        // Avoid re-loading if already present
        if (!document.getElementById('google-gsi-script')) {
          const script = document.createElement('script')
          script.id = 'google-gsi-script'
          script.src = 'https://accounts.google.com/gsi/client'
          script.async = true
          script.defer = true
          document.body.appendChild(script)

          script.onload = () => renderGoogleButton(clientId)
        } else if (window.google) {
          renderGoogleButton(clientId)
        }
      } catch (err) {
        console.error("Failed to load Google Config:", err)
      }
    }

    const renderGoogleButton = (clientId) => {
      if (!window.google) return
      try {
        window.google.accounts.id.initialize({
          client_id: clientId,
          callback: handleCredentialResponse,
          auto_select: false
        })

        const container = document.getElementById('google-official-btn-container')
        if (container) {
          container.innerHTML = '' // Clear previous renders
          window.google.accounts.id.renderButton(container, {
            theme: 'outline',
            size: 'large',
            width: 320,
            shape: 'pill',
            text: 'signin_with'
          })
        }
      } catch (err) {
        console.error("GSI initialization error:", err)
      }
    }

    // Small delay to ensure DOM is ready
    const timer = setTimeout(initGoogleSDK, 100)
    return () => clearTimeout(timer)
  }, [selectedRole])

  // Handler for official Google ID Token responses
  const handleCredentialResponse = async (response) => {
    setLoading(true)
    setError('')
    try {
      const base64Url = response.credential.split('.')[1]
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      )

      const payload = JSON.parse(jsonPayload)

      const authRes = await api.googleLogin({
        token: response.credential,
        email: payload.email,
        name: payload.name,
        role: 'patient' // Always patient for Google Auth
      })

      onLogin(authRes.user, authRes.access_token)
    } catch (err) {
      setError(err.message || 'OAuth verification failed.')
    } finally {
      setLoading(false)
    }
  }

  // ── Clinician: Institutional Code login ──
  const handleClinicianCodeLogin = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await api.clinicianLogin({
        email: clinicianEmail,
        institutional_code: institutionalCode,
        full_name: clinicianName
      })
      onLogin(res.user, res.access_token)
    } catch (err) {
      setError(err.message || 'Invalid institutional code')
    } finally {
      setLoading(false)
    }
  }

  // ── Clinician: Send OTP ──
  const handleSendOTP = async () => {
    setLoading(true)
    setError('')
    try {
      const res = await api.sendOTP({ email: otpEmail })
      setOtpSent(true)
      // Dev mode: show the OTP hint
      if (res.otp_code) {
        setOtpHint(res.otp_code)
      }
    } catch (err) {
      setError(err.message || 'Failed to send OTP')
    } finally {
      setLoading(false)
    }
  }

  // ── Clinician: Verify OTP ──
  const handleVerifyOTP = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await api.verifyOTP({ email: otpEmail, otp_code: otpCode })
      onLogin(res.user, res.access_token)
    } catch (err) {
      setError(err.message || 'Invalid or expired OTP')
    } finally {
      setLoading(false)
    }
  }

  // ── Patient: Register with email/password ──
  const handlePatientRegister = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const username = patientEmail.split('@')[0] + '_' + Math.random().toString(36).slice(2, 6)
      const res = await api.register({
        username,
        email: patientEmail,
        full_name: patientName,
        password: patientPassword,
        role: 'patient'
      })
      onLogin(res.user, res.access_token)
    } catch (err) {
      setError(err.message || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  // ── Shared inline styles ──
  const inputStyle = {
    width: '100%',
    padding: '0.7rem 0.9rem',
    borderRadius: '10px',
    border: '1px solid rgba(0,0,0,0.08)',
    fontSize: '0.85rem',
    background: '#fafafa',
    outline: 'none',
    transition: 'border 150ms ease',
    boxSizing: 'border-box'
  }

  const btnPrimary = {
    width: '100%',
    padding: '0.7rem',
    borderRadius: '10px',
    border: 'none',
    background: 'var(--accent)',
    color: '#fff',
    fontWeight: 700,
    fontSize: '0.85rem',
    cursor: 'pointer',
    transition: 'opacity 150ms ease'
  }

  const dividerLine = (
    <div style={{ display: 'flex', alignItems: 'center', width: '100%', margin: '1.25rem 0', gap: '0.75rem' }}>
      <div style={{ flex: 1, height: '1px', background: 'rgba(0,0,0,0.08)' }} />
      <span style={{ fontSize: '0.7rem', color: '#86868b', fontWeight: 600, letterSpacing: '0.05em' }}>OR</span>
      <div style={{ flex: 1, height: '1px', background: 'rgba(0,0,0,0.08)' }} />
    </div>
  )

  // ── Clinician Auth Form ──
  const renderClinicianForm = () => (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', gap: '0.75rem' }}>
      {/* Clinician sub-mode selector */}
      <div style={{
        display: 'flex', width: '100%', background: '#f0f0f3', borderRadius: '10px',
        padding: '3px', gap: '3px', marginBottom: '0.5rem'
      }}>
        <button
          onClick={() => { setClinicianMode('code'); setError('') }}
          style={{
            flex: 1, padding: '0.5rem', borderRadius: '8px', border: 'none',
            background: clinicianMode === 'code' ? '#fff' : 'transparent',
            color: clinicianMode === 'code' ? '#1d1d1f' : '#86868b',
            fontWeight: 600, fontSize: '0.75rem', cursor: 'pointer',
            boxShadow: clinicianMode === 'code' ? '0 1px 4px rgba(0,0,0,0.06)' : 'none',
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.35rem',
            transition: 'all 150ms ease'
          }}
        >
          <KeyRound size={13} /> Access Code
        </button>
        <button
          onClick={() => { setClinicianMode('otp'); setError(''); setOtpSent(false); setOtpHint('') }}
          style={{
            flex: 1, padding: '0.5rem', borderRadius: '8px', border: 'none',
            background: clinicianMode === 'otp' ? '#fff' : 'transparent',
            color: clinicianMode === 'otp' ? '#1d1d1f' : '#86868b',
            fontWeight: 600, fontSize: '0.75rem', cursor: 'pointer',
            boxShadow: clinicianMode === 'otp' ? '0 1px 4px rgba(0,0,0,0.06)' : 'none',
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.35rem',
            transition: 'all 150ms ease'
          }}
        >
          <Mail size={13} /> Email OTP
        </button>
      </div>

      {clinicianMode === 'code' ? (
        /* ── Institutional Code Form ── */
        <form onSubmit={handleClinicianCodeLogin} style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <input
            type="text"
            placeholder="Full Name"
            value={clinicianName}
            onChange={e => setClinicianName(e.target.value)}
            style={inputStyle}
            onFocus={e => e.target.style.borderColor = 'var(--accent)'}
            onBlur={e => e.target.style.borderColor = 'rgba(0,0,0,0.08)'}
          />
          <input
            type="email"
            placeholder="Institutional Email"
            value={clinicianEmail}
            onChange={e => setClinicianEmail(e.target.value)}
            style={inputStyle}
            onFocus={e => e.target.style.borderColor = 'var(--accent)'}
            onBlur={e => e.target.style.borderColor = 'rgba(0,0,0,0.08)'}
          />
          <input
            type="password"
            placeholder="Institutional Access Code"
            value={institutionalCode}
            onChange={e => setInstitutionalCode(e.target.value)}
            style={inputStyle}
            onFocus={e => e.target.style.borderColor = 'var(--accent)'}
            onBlur={e => e.target.style.borderColor = 'rgba(0,0,0,0.08)'}
          />
          <button
            type="submit"
            disabled={loading || !clinicianEmail || !institutionalCode}
            style={{ ...btnPrimary, opacity: (loading || !clinicianEmail || !institutionalCode) ? 0.5 : 1 }}
          >
            {loading ? 'Authenticating...' : 'Sign In as Clinician'}
          </button>

          {/* Demo hint */}
          <div style={{
            background: 'linear-gradient(135deg, #f0f9ff, #e8f4fd)',
            border: '1px solid rgba(59, 130, 246, 0.15)',
            borderRadius: '8px', padding: '0.6rem 0.75rem',
            display: 'flex', alignItems: 'center', gap: '0.5rem'
          }}>
            <Shield size={14} style={{ color: '#3b82f6', flexShrink: 0 }} />
            <span style={{ fontSize: '0.7rem', color: '#64748b', lineHeight: 1.4 }}>
              Demo code: <strong style={{ color: '#1e40af', fontFamily: 'monospace', letterSpacing: '0.05em' }}>RARESENSE2026</strong>
            </span>
          </div>
        </form>
      ) : (
        /* ── Email OTP Form ── */
        <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <input
            type="email"
            placeholder="Your email address"
            value={otpEmail}
            onChange={e => { setOtpEmail(e.target.value); setOtpSent(false); setOtpHint('') }}
            style={inputStyle}
            onFocus={e => e.target.style.borderColor = 'var(--accent)'}
            onBlur={e => e.target.style.borderColor = 'rgba(0,0,0,0.08)'}
          />

          {!otpSent ? (
            <button
              onClick={handleSendOTP}
              disabled={loading || !otpEmail}
              style={{ ...btnPrimary, opacity: (loading || !otpEmail) ? 0.5 : 1, background: '#1e40af' }}
            >
              {loading ? 'Sending...' : 'Send Verification Code'}
            </button>
          ) : (
            <form onSubmit={handleVerifyOTP} style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {/* OTP hint in dev mode */}
              {otpHint && (
                <div style={{
                  background: 'linear-gradient(135deg, #ecfdf5, #d1fae5)',
                  border: '1px solid rgba(16, 185, 129, 0.2)',
                  borderRadius: '8px', padding: '0.6rem 0.75rem',
                  display: 'flex', alignItems: 'center', gap: '0.5rem'
                }}>
                  <Mail size={14} style={{ color: '#059669', flexShrink: 0 }} />
                  <span style={{ fontSize: '0.7rem', color: '#065f46', lineHeight: 1.4 }}>
                    Dev mode — Your OTP: <strong style={{ fontFamily: 'monospace', letterSpacing: '0.15em', fontSize: '0.85rem' }}>{otpHint}</strong>
                  </span>
                </div>
              )}

              <input
                type="text"
                placeholder="Enter 6-digit code"
                value={otpCode}
                onChange={e => setOtpCode(e.target.value)}
                maxLength={6}
                style={{ ...inputStyle, textAlign: 'center', letterSpacing: '0.3em', fontSize: '1.1rem', fontWeight: 700 }}
                onFocus={e => e.target.style.borderColor = 'var(--accent)'}
                onBlur={e => e.target.style.borderColor = 'rgba(0,0,0,0.08)'}
              />
              <button
                type="submit"
                disabled={loading || otpCode.length !== 6}
                style={{ ...btnPrimary, opacity: (loading || otpCode.length !== 6) ? 0.5 : 1 }}
              >
                {loading ? 'Verifying...' : 'Verify & Sign In'}
              </button>
              <button
                type="button"
                onClick={() => { setOtpSent(false); setOtpCode(''); setOtpHint('') }}
                style={{ background: 'none', border: 'none', color: '#86868b', fontSize: '0.75rem', cursor: 'pointer', textDecoration: 'underline' }}
              >
                Resend code
              </button>
            </form>
          )}
        </div>
      )}
    </div>
  )

  // ── Patient Auth Form ──
  const renderPatientForm = () => (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}>
      {/* Google Sign-In Button (primary) */}
      <div
        id="google-official-btn-container"
        style={{
          width: '100%',
          display: 'flex',
          justifyContent: 'center',
          minHeight: '40px'
        }}
      />

      {dividerLine}

      <div style={{ display: 'flex', alignItems: 'center', width: '100%', marginBottom: '1rem', gap: '0.75rem' }}>
        <div style={{ flex: 1, height: '1px', background: 'rgba(0,0,0,0.08)' }} />
        <span style={{ fontSize: '0.7rem', color: '#86868b', fontWeight: 600, letterSpacing: '0.05em' }}>REGISTER WITH EMAIL</span>
        <div style={{ flex: 1, height: '1px', background: 'rgba(0,0,0,0.08)' }} />
      </div>

      {/* Register form */}
      <form onSubmit={handlePatientRegister} style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        <input
          type="text"
          placeholder="Full Name"
          value={patientName}
          onChange={e => setPatientName(e.target.value)}
          style={inputStyle}
          onFocus={e => e.target.style.borderColor = 'var(--accent)'}
          onBlur={e => e.target.style.borderColor = 'rgba(0,0,0,0.08)'}
        />
        <input
          type="email"
          placeholder="Email"
          value={patientEmail}
          onChange={e => setPatientEmail(e.target.value)}
          style={inputStyle}
          onFocus={e => e.target.style.borderColor = 'var(--accent)'}
          onBlur={e => e.target.style.borderColor = 'rgba(0,0,0,0.08)'}
        />
        <input
          type="password"
          placeholder="Create Password"
          value={patientPassword}
          onChange={e => setPatientPassword(e.target.value)}
          style={inputStyle}
          onFocus={e => e.target.style.borderColor = 'var(--accent)'}
          onBlur={e => e.target.style.borderColor = 'rgba(0,0,0,0.08)'}
        />
        <button
          type="submit"
          disabled={loading || !patientName || !patientEmail || !patientPassword}
          style={{
            ...btnPrimary,
            opacity: (loading || !patientName || !patientEmail || !patientPassword) ? 0.5 : 1,
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem'
          }}
        >
          <UserPlus size={16} />
          {loading ? 'Creating account...' : 'Register & Sign In'}
        </button>
      </form>
    </div>
  )

  return (
    <div className="login-page">
      <div className="login-split-container">
        {/* Left Side: Auth Form */}
        <div className="login-form-pane">
          {/* Floating dynamic background clinician illustration (watermark) */}
          <img
            src="/doctor_treating_patient.png"
            className="clinical-bg-illustration"
            alt="Clinician consulting patient backdrop"
          />

          {/* Form Content container to sit above background z-index */}
          <div style={{ position: 'relative', zIndex: 2, display: 'flex', flexDirection: 'column', width: '100%' }}>
            {/* Brand header */}
            <div className="logo">
              <div className="logo-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" style={{ width: '26px', height: '26px', color: 'var(--accent)' }}>
                  <path d="M4.5 16.5c3-4.5 3-4.5 6-9s3-4.5 6-9" />
                  <path d="M4.5 7.5c3 4.5 3 4.5 6 9s3 4.5 6 9" opacity="0.3" />
                  <circle cx="12" cy="12" r="9" strokeWidth="1.5" strokeDasharray="3 2" />
                  <circle cx="10.5" cy="7.5" r="1.5" fill="var(--accent)" stroke="none" />
                  <circle cx="13.5" cy="16.5" r="1.5" fill="var(--accent)" stroke="none" />
                </svg>
              </div>
              <h2>RareSense.AI</h2>
              <p>{selectedRole === 'clinician' ? 'Institutional Clinical Portal' : 'Patient Health Portal'}</p>
            </div>

            {error && <div className="login-error"><AlertCircle size={14} /> {error}</div>}

            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}>
              {/* Segmented Control for Portal Selection */}
              <div
                className="segmented-control"
                style={{
                  width: '100%',
                  display: 'flex',
                  background: '#f5f5f7',
                  border: '1px solid rgba(0, 0, 0, 0.04)',
                  borderRadius: '12px',
                  padding: '3px',
                  marginBottom: '2rem'
                }}
              >
                <button
                  onClick={() => { setSelectedRole('clinician'); setError('') }}
                  style={{
                    flex: 1,
                    padding: '0.65rem',
                    borderRadius: '10px',
                    border: 'none',
                    background: selectedRole === 'clinician' ? '#ffffff' : 'transparent',
                    color: selectedRole === 'clinician' ? '#1d1d1f' : '#86868b',
                    fontWeight: 700,
                    fontSize: '0.8rem',
                    cursor: 'pointer',
                    boxShadow: selectedRole === 'clinician' ? '0 2px 6px rgba(0,0,0,0.06)' : 'none',
                    transition: 'all 150ms ease',
                    display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem'
                  }}
                >
                  <Shield size={14} /> Clinician Portal
                </button>
                <button
                  onClick={() => { setSelectedRole('patient'); setError('') }}
                  style={{
                    flex: 1,
                    padding: '0.65rem',
                    borderRadius: '10px',
                    border: 'none',
                    background: selectedRole === 'patient' ? '#ffffff' : 'transparent',
                    color: selectedRole === 'patient' ? '#1d1d1f' : '#86868b',
                    fontWeight: 700,
                    fontSize: '0.8rem',
                    cursor: 'pointer',
                    boxShadow: selectedRole === 'patient' ? '0 2px 6px rgba(0,0,0,0.06)' : 'none',
                    transition: 'all 150ms ease',
                    display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem'
                  }}
                >
                  <UserPlus size={14} /> Patient Portal
                </button>
              </div>

              {/* Render the appropriate auth form based on selected role */}
              {selectedRole === 'clinician' ? renderClinicianForm() : renderPatientForm()}

              {loading && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: '#86868b', margin: '1rem 0 0' }}>
                  <RefreshCw size={14} className="spin" style={{ color: 'var(--accent)' }} /> Authenticating...
                </div>
              )}

              <span style={{ fontSize: '0.72rem', color: '#86868b', textAlign: 'center', marginTop: '1.5rem', lineHeight: 1.45, maxWidth: '280px' }}>
                {selectedRole === 'clinician'
                  ? 'Access restricted to authorized medical personnel with institutional credentials.'
                  : 'Patient access is open. Sign in with Google or create an account to view your health data.'}
              </span>
            </div>
          </div>
        </div>

        {/* Right Side: Immersive Clinical diagnostic sequencer display */}
        <div className="login-video-pane">
          {/* Medical grid background coordinates */}
          <div className="clinical-grid-overlay"></div>

          {/* Clinical Monitor Header Indicators */}
          <div className="clinical-monitor-header">
            <span className="indicator-label pulse-light">SYS.MONITOR: OK</span>
            <span className="indicator-label">SEQ_SCANNER_v4.1</span>
          </div>

          {/* Glowing 3D DNA Sequencer Helix */}
          <div className="dopamine-container">
            <div className="clinical-helix-container">
              {helixSegments.map((_, i) => (
                <div key={i} className="clinical-base-pair" style={{ '--i': i }}>
                  <div className="clinical-node node-left"></div>
                  <div className="clinical-bond-line"></div>
                  <div className="clinical-node node-right"></div>
                </div>
              ))}
            </div>
          </div>

          {/* Clinical Monitor Footer Indicators */}
          <div className="clinical-monitor-footer">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
              <span className="sys-term">EMBEDDING_ALIGNMENT: 92.4%</span>
              <span className="sys-term">PHENOTYPIC_DENSITY: NOMINAL</span>
            </div>
            <span className="sys-term tracking-id">PATIENT: P-LUPUS001</span>
          </div>

          <div className="video-overlay-gradient"></div>
          <div className="video-pane-caption">
            <h3>Deciphering Rare Syndromes</h3>
            <p>Mapping complex phenotypes to genetic pathologies via the Orphanet database and BioBERT reasoning.</p>
          </div>
        </div>
      </div>
    </div>
  )
}
