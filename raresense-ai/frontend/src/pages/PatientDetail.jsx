import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../utils/api'
import { 
  ArrowLeft, Plus, Play, Calendar, User, Droplet, FileText, Dna, 
  AlertTriangle, CheckCircle, XCircle, Clock, Edit, Trash2, Eye, 
  FileSpreadsheet, Image, Activity, FileDigit, Heart, Download, 
  Check, X, ChevronDown, ChevronUp, AlertCircle, RefreshCw, Layers
} from 'lucide-react'

export default function PatientDetail({ user }) {
  const { id } = useParams()
  const navigate = useNavigate()
  const [patient, setPatient] = useState(null)
  const [timeline, setTimeline] = useState(null)
  const [matches, setMatches] = useState([])
  const [tab, setTab] = useState('timeline')
  const [loading, setLoading] = useState(true)
  const [matching, setMatching] = useState(false)
  const [updatingMatch, setUpdatingMatch] = useState(null) // matchId being updated

  const isClinician = user?.role !== 'patient'
  
  // Note Modal States
  const [showNoteModal, setShowNoteModal] = useState(false)
  const [editNoteId, setEditNoteId] = useState(null)
  const [noteForm, setNoteForm] = useState({
    note_type: 'consultation',
    specialty: 'General',
    physician: '',
    date: '',
    text: '',
    reports: []
  })
  
  // Temporary Report Fields (inside the note modal)
  const [showAddReportForm, setShowAddReportForm] = useState(false)
  const [reportForm, setReportForm] = useState({
    name: '',
    type: 'lab',
    status: 'normal',
    summary: ''
  })
  
  // Report Viewer Console Modal States
  const [showReportViewer, setShowReportViewer] = useState(false)
  const [activeReport, setActiveReport] = useState(null)
  const [isScanning, setIsScanning] = useState(false)
  const [scanProgress, setScanProgress] = useState(0)
  const [scanLogs, setScanLogs] = useState([])
  
  // Advanced Visualizer Interactive States
  const [mriSlice, setMriSlice] = useState(11)
  const [dnaPhase, setDnaPhase] = useState(0)
  const [selectedBiomarker, setSelectedBiomarker] = useState('PLT')
  const [heartRate, setHeartRate] = useState(74)
  
  // Note text expand state
  const [expandedNotes, setExpandedNotes] = useState({})

  useEffect(() => { loadPatient() }, [id])

  // 3D DNA Rotation Loop
  useEffect(() => {
    let animFrame
    const tick = () => {
      setDnaPhase(p => (p + 0.015) % (Math.PI * 2))
      animFrame = requestAnimationFrame(tick)
    }
    if (showReportViewer && activeReport?.type === 'genetics' && !isScanning) {
      animFrame = requestAnimationFrame(tick)
    }
    return () => cancelAnimationFrame(animFrame)
  }, [showReportViewer, activeReport, isScanning])

  async function loadPatient() {
    setLoading(true)
    try {
      const [p, tl, m] = await Promise.all([
        api.getPatient(id),
        api.getTimeline(id),
        api.getMatchResults(id).catch(() => ({ matches: [] })),
      ])
      setPatient(p)
      setTimeline(tl)
      setMatches(m.matches || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  async function runMatching() {
    setMatching(true)
    try {
      const result = await api.runMatching(id)
      setMatches(result.matches || [])
      setTab('matches')
    } catch (err) {
      alert(err.message)
    } finally {
      setMatching(false)
    }
  }

  async function handleApproveMatch(matchId, currentStatus) {
    const newStatus = currentStatus === 'confirmed' ? 'pending' : 'confirmed'
    setUpdatingMatch(matchId)
    try {
      await api.updateMatchStatus(matchId, newStatus)
      setMatches(prev => prev.map(m => m.match_id === matchId ? { ...m, status: newStatus } : m))
    } catch (err) {
      alert(err.message)
    } finally {
      setUpdatingMatch(null)
    }
  }

  async function handleDismissMatch(matchId) {
    setUpdatingMatch(matchId)
    try {
      await api.updateMatchStatus(matchId, 'dismissed')
      setMatches(prev => prev.map(m => m.match_id === matchId ? { ...m, status: 'dismissed' } : m))
    } catch (err) {
      alert(err.message)
    } finally {
      setUpdatingMatch(null)
    }
  }

  // Add / Edit note submission
  async function handleSubmitNote(e) {
    e.preventDefault()
    try {
      const payload = {
        note_type: noteForm.note_type,
        specialty: noteForm.specialty,
        physician: noteForm.physician,
        date: new Date(noteForm.date).toISOString(),
        text: noteForm.text,
        reports: noteForm.reports || []
      }
      
      if (editNoteId) {
        await api.updateClinicalNote(editNoteId, payload)
      } else {
        await api.addNote(id, payload)
      }
      
      setShowNoteModal(false)
      setEditNoteId(null)
      setNoteForm({ note_type: 'consultation', specialty: 'General', physician: '', date: '', text: '', reports: [] })
      loadPatient()
    } catch (err) {
      alert(err.message)
    }
  }

  function handleAddNoteClick() {
    setEditNoteId(null)
    setNoteForm({
      note_type: 'consultation',
      specialty: 'General',
      physician: '',
      date: new Date().toISOString().substring(0, 10),
      text: '',
      reports: []
    })
    setShowNoteModal(true)
  }

  function handleEditNoteClick(entry) {
    setEditNoteId(entry.note_id)
    setNoteForm({
      note_type: entry.note_type || 'consultation',
      specialty: entry.specialty || 'General',
      physician: entry.physician || '',
      date: entry.date ? new Date(entry.date).toISOString().substring(0, 10) : '',
      text: entry.summary || '', // full text is projected
      reports: entry.reports || []
    })
    setShowNoteModal(true)
  }

  async function handleDeleteNoteClick(noteId) {
    if (window.confirm("Are you sure you want to delete this clinical timeline entry? All extracted medical entities will be removed and matching recalculated.")) {
      try {
        await api.deleteClinicalNote(noteId)
        loadPatient()
      } catch (err) {
        alert(err.message)
      }
    }
  }

  // Report attachment management inside note modal
  function handleAddReport(e) {
    e.preventDefault()
    if (!reportForm.name.trim()) return
    
    const newReportItem = {
      report_id: `R-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      name: reportForm.name.trim(),
      type: reportForm.type,
      status: reportForm.status,
      summary: reportForm.summary.trim(),
      file_name: `${reportForm.name.toLowerCase().trim().replace(/[^a-z0-9]+/g, '_')}_result.pdf`,
      uploaded_at: new Date().toISOString()
    }
    
    setNoteForm(prev => ({
      ...prev,
      reports: [...(prev.reports || []), newReportItem]
    }))
    
    // Reset report form
    setReportForm({
      name: '',
      type: 'lab',
      status: 'normal',
      summary: ''
    })
    setShowAddReportForm(false)
  }

  function handleRemoveReport(reportId) {
    setNoteForm(prev => ({
      ...prev,
      reports: (prev.reports || []).filter(r => r.report_id !== reportId)
    }))
  }

  // View report console with scanning telemetry simulation
  function handleViewReportClick(report) {
    setActiveReport(report)
    setShowReportViewer(true)
    setIsScanning(true)
    setScanProgress(0)
    setMriSlice(11) // Reset slider
    setSelectedBiomarker('PLT') // Reset selection
    setHeartRate(74) // Reset rate
    setScanLogs([
      "INITIALIZING SCAN ENGINE...",
      "ACQUIRING CRYPTO HASH SHA-256...",
      "ESTABLISHING BIOMETRIC CORRELATION..."
    ])
  }

  // Scanning simulation runner
  useEffect(() => {
    let timer
    if (isScanning && showReportViewer) {
      const logs = [
        "PARSING HIERARCHICAL SCHEMA...",
        "DECRYPTING CLINICAL METRICS...",
        "DEVICES SYNCHRONIZED [OK]",
        "CALIBRATING SENSOR CODES...",
        "COMPILING BIOMARKER OVERLAYS...",
        "RESOLVING LAB RANGES [OK]",
        "AI ANOMALY SCANNING EN ROUTE...",
        "RENDERING PATHOLOGY MATRIX...",
        "GENERATING DIAGNOSTIC REPORT [OK]"
      ]
      
      timer = setInterval(() => {
        setScanProgress(prev => {
          if (prev >= 100) {
            clearInterval(timer)
            setIsScanning(false)
            return 100
          }
          const step = Math.floor(Math.random() * 15) + 5
          const newProg = Math.min(prev + step, 100)
          
          // Add random logs matching progress
          const logIdx = Math.floor((newProg / 100) * logs.length)
          const newLogs = logs.slice(0, logIdx + 1)
          setScanLogs([
            "INITIALIZING SCAN ENGINE...",
            "ACQUIRING CRYPTO HASH SHA-256...",
            "ESTABLISHING BIOMETRIC CORRELATION...",
            ...newLogs
          ])
          
          return newProg
        })
      }, 70)
    }
    return () => clearInterval(timer)
  }, [isScanning, showReportViewer])

  function toggleNoteExpand(noteId) {
    setExpandedNotes(prev => ({
      ...prev,
      [noteId]: !prev[noteId]
    }))
  }

  // 3D DNA Projection renderer (pure mathematical vector design)
  const renderDnaStrands = () => {
    const nodes = 10
    const width = 300
    const height = 120
    const centerY = height / 2
    const spacing = width / (nodes + 1)
    
    return [...Array(nodes)].map((_, i) => {
      const x = spacing + i * spacing
      const nodeAngle = (i / nodes) * Math.PI * 2.5 + dnaPhase
      
      const cos = Math.cos(nodeAngle)
      const sin = Math.sin(nodeAngle)
      
      const radius = 32
      const y1 = centerY + cos * radius
      const y2 = centerY - cos * radius
      
      // Depth calculations
      const z1 = sin
      const z2 = -sin
      
      const isMutated = i === 2 || i === 6
      const r1 = 3.5 + z1 * 1.5
      const r2 = 3.5 + z2 * 1.5
      
      const opacity1 = 0.45 + (z1 + 1) * 0.25
      const opacity2 = 0.45 + (z2 + 1) * 0.25
      
      return (
        <g key={i}>
          <line 
            x1={x} 
            y1={y1} 
            x2={x} 
            y2={y2} 
            stroke={isMutated ? "var(--warning)" : "rgba(15, 23, 42, 0.12)"} 
            strokeWidth={isMutated ? 2.5 : 1} 
            opacity={Math.min(opacity1, opacity2)} 
            strokeDasharray={isMutated ? "none" : "2 2"} 
          />
          {z1 < z2 ? (
            <>
              <circle cx={x} cy={y1} r={r1} fill={isMutated ? "var(--warning)" : "var(--accent)"} opacity={opacity1} className={isMutated ? "dna-mutated-pulse" : ""} />
              <circle cx={x} cy={y2} r={r2} fill={isMutated ? "var(--warning)" : "var(--info)"} opacity={opacity2} className={isMutated ? "dna-mutated-pulse" : ""} />
            </>
          ) : (
            <>
              <circle cx={x} cy={y2} r={r2} fill={isMutated ? "var(--warning)" : "var(--info)"} opacity={opacity2} className={isMutated ? "dna-mutated-pulse" : ""} />
              <circle cx={x} cy={y1} r={r1} fill={isMutated ? "var(--warning)" : "var(--accent)"} opacity={opacity1} className={isMutated ? "dna-mutated-pulse" : ""} />
            </>
          )}
          {isMutated && (
            <g transform={`translate(${x - 20}, ${y1 < y2 ? y1 - 20 : y2 - 20})`}>
              <rect x="0" y="0" width="40" height="12" rx="2" fill="#ffffff" stroke="var(--warning)" strokeWidth="0.5" />
              <text x="20" y="9" fill="var(--warning)" fontSize="6" fontWeight="bold" textAnchor="middle" fontFamily="monospace">ALLELE</text>
            </g>
          )}
        </g>
      )
    })
  }

  // Imaging geometry scale adjustments based on active slice
  const mriSliceScale = 1.0 - Math.abs(11 - mriSlice) * 0.02
  const ventricleScale = 1.0 - Math.abs(11 - mriSlice) * 0.04
  const lesionRadius = Math.max(0, 3.5 - Math.abs(11 - mriSlice) * 0.4)
  const lesionX = 160 + (11 - mriSlice) * 1.5
  const lesionY = 140 + (11 - mriSlice) * 1.0

  if (loading) return <div className="loading-container"><div className="spinner" /></div>
  if (!patient) return <div className="empty-state"><h3>Patient not found</h3></div>

  const age = patient.date_of_birth ? Math.floor((Date.now() - new Date(patient.date_of_birth)) / 31557600000) : '?'

  const selectedBiomarkerHistory = {
    PLT: { name: 'Platelets (PLT)', values: [120, 105, 98, 92], unit: '/ µL', desc: 'Autoimmune destruction of platelets.' },
    WBC: { name: 'White Blood Cells', values: [9.5, 11.2, 12.0, 12.4], unit: 'x10^3/µL', desc: 'Systemic inflammation activity indicator.' },
    CRP: { name: 'C-Reactive Protein', values: [12.4, 28.0, 39.5, 42.5], unit: 'mg/L', desc: 'Acute phase inflammatory protein.' }
  }[selectedBiomarker] || { name: 'Platelets (PLT)', values: [120, 105, 98, 92], unit: '/ µL', desc: '' }

  return (
    <div className="fade-in workspace-glow-bg">
      {/* Back button */}
      <button className="btn btn-secondary btn-sm" onClick={() => navigate('/patients')} style={{ marginBottom: '1.25rem', display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}>
        <ArrowLeft size={14} /> Back to Patients
      </button>

      {/* Patient Header */}
      <div className="patient-header-card glassmorphic-panel">
        <div className="patient-avatar-lg glowing-avatar-border">
          {patient.first_name?.[0]}{patient.last_name?.[0]}
        </div>
        <div style={{ flex: 1 }}>
          <h2 style={{ fontSize: '1.65rem', fontWeight: 800, letterSpacing: '-0.3px', color: 'var(--text-primary)' }}>
            {patient.first_name} {patient.last_name}
          </h2>
          <div className="patient-meta">
            <div className="patient-meta-item"><User size={13} />{age} yrs, {patient.gender === 'F' ? 'Female' : patient.gender === 'M' ? 'Male' : patient.gender}</div>
            {patient.blood_type && <div className="patient-meta-item"><Droplet size={13} />{patient.blood_type}</div>}
            <div className="patient-meta-item"><FileText size={13} />{patient.notes_count || 0} Notes</div>
            <div className="patient-meta-item"><Dna size={13} />{matches.length} Matches</div>
            <div className="patient-meta-item"><Calendar size={13} />ID: {patient.patient_id}</div>
          </div>
        </div>
        {isClinician && (
          <div style={{ display: 'flex', gap: '0.65rem' }}>
            <button className="btn btn-primary btn-glow" onClick={runMatching} disabled={matching}>
              {matching ? <><RefreshCw size={14} className="spin" /> Matching...</> : <><Play size={14} /> Run AI Matching</>}
            </button>
            <button className="btn btn-secondary" onClick={handleAddNoteClick}>
              <Plus size={14} /> Add Note
            </button>
          </div>
        )}
      </div>

      {/* Patient Info Cards */}
      <div className="grid-3" style={{ marginBottom: '1.75rem' }}>
        <div className="card glassmorphic-panel hover-card-rise">
          <h4 className="info-card-header">Medical History</h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem' }}>
            {(patient.medical_history || []).length > 0
              ? patient.medical_history.map((h, i) => <span key={i} className="badge badge-warning badge-glow">{h}</span>)
              : <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>No history</span>}
          </div>
        </div>
        <div className="card glassmorphic-panel hover-card-rise">
          <h4 className="info-card-header">Current Medications</h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem' }}>
            {(patient.current_medications || []).length > 0
              ? patient.current_medications.map((m, i) => <span key={i} className="entity-tag medication">{m}</span>)
              : <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>None</span>}
          </div>
        </div>
        <div className="card glassmorphic-panel hover-card-rise">
          <h4 className="info-card-header">Allergies</h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem' }}>
            {(patient.allergies || []).length > 0
              ? patient.allergies.map((a, i) => <span key={i} className="badge badge-danger badge-glow">{a}</span>)
              : <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>None known</span>}
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button className={`tab ${tab === 'timeline' ? 'active' : ''}`} onClick={() => setTab('timeline')}>Timeline ({timeline?.total_visits || 0})</button>
        {isClinician && (
          <button className={`tab ${tab === 'matches' ? 'active' : ''}`} onClick={() => setTab('matches')}>AI Disease Matches ({matches.length})</button>
        )}
      </div>

      {/* Timeline Tab */}
      {tab === 'timeline' && (
        <div className="timeline-container">
          <div className="timeline-trail-line" />
          <div className="timeline">
            {timeline?.timeline?.length > 0 ? timeline.timeline.map((entry, i) => (
              <div key={i} className="timeline-item slide-in-timeline">
                <div className="timeline-node pulsing-glow" />
                <div className="timeline-date">
                  <Calendar size={12} style={{ display: 'inline', marginRight: '0.4rem', verticalAlign: 'text-bottom' }} />
                  {new Date(entry.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
                  <span className="badge badge-info" style={{ marginLeft: '0.75rem' }}>{entry.specialty}</span>
                  <span className="badge badge-accent" style={{ marginLeft: '0.4rem' }}>{entry.note_type?.replace(/_/g, ' ')}</span>
                </div>
                <div className="timeline-card glassmorphic-panel hover-glow-border">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                    <div>
                      <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-primary)' }}>{entry.specialty} — {entry.note_type?.replace(/_/g, ' ')}</h4>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Visited {entry.physician || 'Physician'}</span>
                    </div>
                    {isClinician && (
                      <div className="timeline-actions">
                        <button className="action-btn text-info" onClick={() => handleEditNoteClick(entry)} title="Edit clinical note">
                          <Edit size={14} />
                        </button>
                        <button className="action-btn text-danger" onClick={() => handleDeleteNoteClick(entry.note_id)} title="Delete event">
                          <Trash2 size={14} />
                        </button>
                      </div>
                    )}
                  </div>
                  
                  {/* Note Body with Read More Toggle */}
                  <div className="timeline-text-content" style={{ marginBottom: '1rem' }}>
                    <p className="clinical-text-font" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>
                      {expandedNotes[entry.note_id] || (entry.summary || '').length <= 220
                        ? entry.summary 
                        : `${entry.summary.substring(0, 220)}...`}
                    </p>
                    {(entry.summary || '').length > 220 && (
                      <button className="read-more-btn" onClick={() => toggleNoteExpand(entry.note_id)}>
                        {expandedNotes[entry.note_id] ? <>Show Less <ChevronUp size={12} /></> : <>Read More <ChevronDown size={12} /></>}
                      </button>
                    )}
                  </div>
                  
                  {/* Extracted entities */}
                  {((entry.symptoms || []).length > 0 || (entry.medications || []).length > 0 || (entry.diagnoses || []).length > 0 || (entry.lab_values || []).length > 0) && (
                    <div className="timeline-entities">
                      {entry.symptoms?.map((s, j) => (
                        <span key={j} className="entity-tag symptom" title={s.hpo_code || 'Symptom'}>
                          {s.normalized_name}
                        </span>
                      ))}
                      {entry.medications?.map((m, j) => (
                        <span key={j} className="entity-tag medication">
                          {m.normalized_name}
                        </span>
                      ))}
                      {entry.diagnoses?.map((d, j) => (
                        <span key={j} className="entity-tag diagnosis">
                          {d.normalized_name}
                        </span>
                      ))}
                      {entry.lab_values?.map((l, j) => (
                        <span key={j} className="entity-tag lab_value">
                          {l.normalized_name}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Attached Reports Section */}
                  {entry.reports && entry.reports.length > 0 && (
                    <div className="timeline-reports-section" style={{ marginTop: '1rem', paddingTop: '0.85rem', borderTop: '1px solid var(--border)' }}>
                      <span className="section-mini-title"><Layers size={11} style={{ marginRight: '0.3rem' }} /> Linked Reports ({entry.reports.length})</span>
                      <div className="reports-flex-grid">
                        {entry.reports.map((rep, j) => (
                          <div key={j} className={`report-badge-card report-status-${rep.status}`} onClick={() => handleViewReportClick(rep)}>
                            <div className="report-badge-icon">
                              {rep.type === 'lab' && <FileSpreadsheet size={15} />}
                              {rep.type === 'imaging' && <Image size={15} />}
                              {rep.type === 'genetics' && <Dna size={15} />}
                              {rep.type === 'prescription' && <FileDigit size={15} />}
                              {rep.type !== 'lab' && rep.type !== 'imaging' && rep.type !== 'genetics' && rep.type !== 'prescription' && <FileText size={15} />}
                            </div>
                            <div className="report-badge-text">
                              <div className="report-badge-name">{rep.name}</div>
                              <div className="report-badge-category">{rep.type.toUpperCase()} • {rep.status.toUpperCase()}</div>
                            </div>
                            <Eye size={12} className="report-badge-view-arrow" />
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )) : (
              <div className="empty-state glassmorphic-panel">
                <FileText size={48} className="empty-state-icon" />
                <h3>No clinical notes in timeline</h3>
                <p>Create a clinical timeline entry to scan patient files and map HPO symptoms.</p>
                <button className="btn btn-primary" onClick={handleAddNoteClick} style={{ marginTop: '1rem' }}>
                  <Plus size={14} /> Add First Note
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Matches Tab — Clinicians only */}
      {tab === 'matches' && isClinician && (
        <div className="fade-in">
          {/* Info banner */}
          <div style={{
            background: 'rgba(99,102,241,0.05)',
            border: '1px solid rgba(99,102,241,0.15)',
            borderRadius: 'var(--radius-md)',
            padding: '0.75rem 1rem',
            marginBottom: '1.25rem',
            fontSize: '0.82rem',
            color: 'var(--text-secondary)',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <CheckCircle size={15} style={{ color: 'var(--accent)', flexShrink: 0 }} />
            Approve a match to make it visible on the patient's health portal. Dismissed matches are hidden from patients.
          </div>

          {matches.length > 0 ? matches.map((match, i) => {
            const confPct = Math.round(match.confidence * 100)
            const level = confPct >= 60 ? 'high' : confPct >= 30 ? 'medium' : 'low'
            const isConfirmed = match.status === 'confirmed'
            const isDismissed = match.status === 'dismissed'
            const isUpdating = updatingMatch === match.match_id
            return (
              <div key={i} className={`match-card glassmorphic-panel hover-glow-border ${level}`} style={{
                opacity: isDismissed ? 0.45 : 1,
                transition: 'opacity 0.2s'
              }}>
                <div className="match-header">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', flex: 1 }}>
                    <div className="match-rank">{match.rank}</div>
                    <div>
                      <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-primary)' }}>{match.disease_name}</h3>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>{match.disease_orpha_id}</span>
                    </div>
                    {isConfirmed && (
                      <span className="badge badge-success" style={{ fontSize: '0.65rem', padding: '0.2rem 0.6rem' }}>
                        <CheckCircle size={10} style={{ marginRight: '0.2rem' }} /> Approved — Visible to Patient
                      </span>
                    )}
                    {isDismissed && (
                      <span className="badge badge-danger" style={{ fontSize: '0.65rem', opacity: 0.7 }}>Dismissed</span>
                    )}
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: 800, color: level === 'high' ? 'var(--success)' : level === 'medium' ? 'var(--warning)' : 'var(--text-tertiary)' }}>
                      {confPct}%
                    </div>
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>confidence</span>
                  </div>
                </div>
                <div className="confidence-bar">
                  <div className={`confidence-fill ${level}`} style={{ width: `${confPct}%` }} />
                </div>
                <div style={{ marginTop: '0.75rem', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                  <strong>{match.matched_count}</strong> of {match.total_disease_symptoms} symptoms matched:
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.4rem', marginBottom: '0.85rem' }}>
                  {match.matched_symptoms?.map((s, j) => (
                    <span key={j} className="entity-tag symptom">{s.symptom_name}</span>
                  ))}
                </div>

                {/* Clinician action buttons */}
                <div style={{ display: 'flex', gap: '0.5rem', borderTop: '1px solid var(--border)', paddingTop: '0.75rem' }}>
                  <button
                    className={`btn btn-sm ${isConfirmed ? 'btn-secondary' : 'btn-primary btn-glow'}`}
                    onClick={() => handleApproveMatch(match.match_id, match.status)}
                    disabled={isUpdating || isDismissed}
                    style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}
                  >
                    <CheckCircle size={13} />
                    {isUpdating ? 'Updating...' : isConfirmed ? 'Revoke Approval' : 'Approve for Patient'}
                  </button>
                  {!isDismissed && !isConfirmed && (
                    <button
                      className="btn btn-sm btn-secondary"
                      onClick={() => handleDismissMatch(match.match_id)}
                      disabled={isUpdating}
                      style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--danger)' }}
                    >
                      <XCircle size={13} /> Dismiss
                    </button>
                  )}
                </div>
              </div>
            )
          }) : (
            <div className="empty-state glassmorphic-panel">
              <Dna size={48} className="empty-state-icon" />
              <h3>No matched diseases</h3>
              <p>Click "Run AI Matching" above to trigger diagnostic reasoning logic against Orphadata rare diseases.</p>
              <button className="btn btn-primary" onClick={runMatching} disabled={matching} style={{ marginTop: '1rem' }}>
                <Play size={14} /> Run AI Matching Engine
              </button>
            </div>
          )}
        </div>
      )}

      {/* Add / Edit Note Modal */}
      {/* Note modal — clinicians only */}
      {showNoteModal && isClinician && (
        <div className="modal-overlay" onClick={() => setShowNoteModal(false)}>
          <div className="modal glassmorphic-panel slide-up-modal" onClick={e => e.stopPropagation()} style={{ maxWidth: '750px', width: '95%' }}>
            <div className="modal-header">
              <h2>{editNoteId ? 'Edit Clinical Event' : 'Add Clinical Note'}</h2>
              <button className="modal-close" onClick={() => setShowNoteModal(false)}><X size={18} /></button>
            </div>
            <form onSubmit={handleSubmitNote}>
              <div className="modal-body">
                <div className="grid-2">
                  <div className="form-group">
                    <label>Note Type</label>
                    <select className="form-select" value={noteForm.note_type} onChange={e => setNoteForm({ ...noteForm, note_type: e.target.value })}>
                      <option value="consultation">Consultation Note</option>
                      <option value="discharge_summary">Discharge Summary</option>
                      <option value="progress_note">Progress Note</option>
                      <option value="radiology">Radiology Report</option>
                      <option value="prescription_upload">Prescription Record</option>
                      <option value="surgery">Surgery Details</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Specialty Department</label>
                    <select className="form-select" value={noteForm.specialty} onChange={e => setNoteForm({ ...noteForm, specialty: e.target.value })}>
                      {['General', 'Dermatology', 'Hematology', 'Nephrology', 'Primary Care', 'Rheumatology', 'Neurology', 'Cardiology', 'Pulmonology', 'Endocrinology', 'Gastroenterology', 'Immunology', 'Radiology', 'Genetics'].map(s => (
                        <option key={s} value={s}>{s}</option>
                      ))}
                    </select>
                  </div>
                </div>
                <div className="grid-2">
                  <div className="form-group">
                    <label>Attending Physician</label>
                    <input className="form-input" required placeholder="Dr. Sarah Connor" value={noteForm.physician} onChange={e => setNoteForm({ ...noteForm, physician: e.target.value })} />
                  </div>
                  <div className="form-group">
                    <label>Date of Visit</label>
                    <input className="form-input" type="date" required value={noteForm.date} onChange={e => setNoteForm({ ...noteForm, date: e.target.value })} />
                  </div>
                </div>
                
                <div className="form-group">
                  <label>Clinical Note Text</label>
                  <textarea
                    className="form-textarea"
                    rows={6}
                    required
                    placeholder="Enter patient narrative notes (e.g. Patient complains of severe joint pain and morning stiffness. Observed butterfly rash on cheeks...)"
                    value={noteForm.text}
                    onChange={e => setNoteForm({ ...noteForm, text: e.target.value })}
                  />
                  <span className="form-help-text">
                    NLP entity engine runs automatically on save to parse symptoms, medications, diagnoses, and lab values.
                  </span>
                </div>

                {/* Note Modal Reports Section */}
                <div className="modal-reports-container" style={{ marginTop: '1.25rem', paddingTop: '1.25rem', borderTop: '1px solid var(--border)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                    <h4 style={{ fontSize: '0.85rem', color: 'var(--text-primary)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Linked Lab/Imaging Reports ({noteForm.reports?.length || 0})</h4>
                    {!showAddReportForm && (
                      <button type="button" className="btn btn-secondary btn-sm" onClick={() => setShowAddReportForm(true)}>
                        <Plus size={12} /> Attach Report
                      </button>
                    )}
                  </div>

                  {/* Add Report Drawer Form */}
                  {showAddReportForm && (
                    <div className="add-report-drawer-panel glassmorphic-panel">
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                        <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--accent-light)' }}>ATTACH NEW MEDICAL REPORT</span>
                        <button type="button" className="action-btn text-muted" onClick={() => setShowAddReportForm(false)}><X size={14} /></button>
                      </div>
                      <div className="grid-2">
                        <div className="form-group">
                          <label style={{ fontSize: '0.7rem' }}>Report Name</label>
                          <input className="form-input form-input-sm" placeholder="e.g. Brain MRI T2 Contrast" value={reportForm.name} onChange={e => setReportForm({ ...reportForm, name: e.target.value })} />
                        </div>
                        <div className="form-group">
                          <label style={{ fontSize: '0.7rem' }}>Report Type</label>
                          <select className="form-select form-select-sm" value={reportForm.type} onChange={e => setReportForm({ ...reportForm, type: e.target.value })}>
                            <option value="lab">Laboratory Panel</option>
                            <option value="imaging">Radiology / Imaging Scan</option>
                            <option value="genetics">Genetics / DNA Profile</option>
                            <option value="prescription">Prescription Slip</option>
                          </select>
                        </div>
                      </div>
                      <div className="grid-2">
                        <div className="form-group">
                          <label style={{ fontSize: '0.7rem' }}>Clinical Status</label>
                          <select className="form-select form-select-sm" value={reportForm.status} onChange={e => setReportForm({ ...reportForm, status: e.target.value })}>
                            <option value="normal">Normal (Within Reference)</option>
                            <option value="abnormal">Abnormal findings</option>
                            <option value="critical">Critical pathology alert</option>
                          </select>
                        </div>
                        <div className="form-group">
                          <label style={{ fontSize: '0.7rem' }}>Diagnostic Summary (Optional)</label>
                          <input className="form-input form-input-sm" placeholder="e.g. Mild inflammation, negative lesions" value={reportForm.summary} onChange={e => setReportForm({ ...reportForm, summary: e.target.value })} />
                        </div>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem', marginTop: '0.25rem' }}>
                        <button type="button" className="btn btn-secondary btn-sm" onClick={() => setShowAddReportForm(false)}>Cancel</button>
                        <button type="button" className="btn btn-primary btn-sm" onClick={handleAddReport} disabled={!reportForm.name.trim()}>Save Attachment</button>
                      </div>
                    </div>
                  )}

                  {/* Attached Reports List */}
                  {noteForm.reports && noteForm.reports.length > 0 ? (
                    <div className="modal-attached-reports-grid">
                      {noteForm.reports.map((rep, idx) => (
                        <div key={idx} className={`attached-rep-row rep-status-${rep.status}`}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flex: 1, minWidth: 0 }}>
                            <div className="rep-row-icon">
                              {rep.type === 'lab' && <FileSpreadsheet size={14} />}
                              {rep.type === 'imaging' && <Image size={14} />}
                              {rep.type === 'genetics' && <Dna size={14} />}
                              {rep.type === 'prescription' && <FileDigit size={14} />}
                              {rep.type !== 'lab' && rep.type !== 'imaging' && rep.type !== 'genetics' && rep.type !== 'prescription' && <FileText size={14} />}
                            </div>
                            <div style={{ minWidth: 0 }}>
                              <div className="rep-row-name" style={{ textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', fontSize: '0.8rem', fontWeight: 600 }}>{rep.name}</div>
                              <div className="rep-row-type" style={{ fontSize: '0.65rem', color: 'var(--text-tertiary)' }}>{rep.type.toUpperCase()} • {rep.status.toUpperCase()}</div>
                            </div>
                          </div>
                          <button type="button" className="action-btn text-danger" onClick={() => handleRemoveReport(rep.report_id)} title="Remove report">
                            <Trash2 size={13} />
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="modal-attached-reports-empty">
                      No documents attached. Clinicians can link diagnostic reports for interactive inspection.
                    </div>
                  )}
                </div>
              </div>
              
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowNoteModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary btn-glow">
                  {editNoteId ? <><Check size={14} /> Save Changes</> : <><Plus size={14} /> Add note</>}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Simulated AI Diagnostic Scan Console / Report Viewer Modal */}
      {showReportViewer && activeReport && (
        <div className="modal-overlay" onClick={() => { setShowReportViewer(false); setActiveReport(null); }}>
          <div className="modal glassmorphic-panel report-viewer-modal slide-up-modal" onClick={e => e.stopPropagation()} style={{ maxWidth: '850px', width: '92%' }}>
            
            {/* Viewport content */}
            {isScanning ? (
              /* SCANNING HUD VIEW */
              <div className="hud-scanner-viewport">
                {/* Elegant circular progress loader ring */}
                <div className="circular-progress-hud">
                  <svg viewBox="0 0 100 100" className="progress-ring-svg">
                    <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(15, 23, 42, 0.02)" strokeWidth="4" />
                    <circle cx="50" cy="50" r="42" fill="none" stroke="var(--accent)" strokeWidth="4" 
                      strokeDasharray="264" strokeDashoffset={264 - (264 * scanProgress) / 100}
                      strokeLinecap="round" className="progress-ring-circle" />
                  </svg>
                  <div className="progress-ring-text">
                    <span className="pct-num">{scanProgress}%</span>
                    <span className="pct-label">SCAN</span>
                  </div>
                </div>
                
                <div className="hud-scanning-progress">
                  <div className="hud-progress-header" style={{ justifyContent: 'center' }}>
                    <span className="pulsate-text">DIAGNOSTIC TELEMETRY CAPTURE...</span>
                  </div>
                </div>

                <div className="hud-console-logs">
                  {scanLogs.map((log, idx) => (
                    <div key={idx} className="console-line">{log}</div>
                  ))}
                  <div className="console-cursor" />
                </div>
              </div>
            ) : (
              /* COMPLETED REPORT VIEW (HIGH INSPIRATION UI) */
              <div className="report-full-console fade-in">
                
                {/* Header Block */}
                <div className="report-console-header">
                  <div>
                    <span className="report-label-code">{activeReport.report_id} // CLINICAL-STATION</span>
                    <h2 className="report-main-title">{activeReport.name}</h2>
                    <div className="report-meta-grid">
                      <div><span>DATE:</span> {new Date(activeReport.uploaded_at || new Date()).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })}</div>
                      <div><span>FILE:</span> {activeReport.file_name}</div>
                      <div><span>STATION:</span> RareSense workstation v2.0</div>
                    </div>
                  </div>
                  <div className="report-console-badge-wrapper">
                    <div className={`report-status-halo status-${activeReport.status}`}>
                      <div className="halo-core">{activeReport.status.toUpperCase()}</div>
                    </div>
                  </div>
                </div>

                {/* Primary Content: Dynamic Visualizer based on Report Type */}
                <div className="report-visualizer-container" style={{ margin: '1.25rem 0', minHeight: '300px' }}>
                  
                  {/* IMAGING REPORT DOCK */}
                  {activeReport.type === 'imaging' && (
                    <div className="imaging-visualizer-dock">
                      <div className="scan-viewport-panel">
                        <div className="viewport-scanning-lines" />
                        <div className="viewport-grid-mesh" />
                        
                        {/* Simulation of a CT/MRI Scan */}
                        <div className="viewport-mri-scan" style={{ position: 'relative', width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          <svg viewBox="0 0 400 300" className="mri-scan-svg" style={{ width: '100%', height: '100%', zIndex: 2 }}>
                            {/* Head Outline (Pure Vector Geometry) */}
                            <path d="M 200,50 C 120,50 80,100 80,180 C 80,240 120,260 200,260 C 280,260 320,240 320,180 C 320,100 280,50 200,50 Z" 
                              fill="none" stroke="rgba(15, 23, 42, 0.12)" strokeWidth="1.25" 
                              transform={`translate(200, 150) scale(${mriSliceScale}) translate(-200, -150)`} />
                            
                            {/* Inner Ventricles Line Overlay */}
                            <path d="M 200,80 C 140,80 110,120 110,180 C 110,225 140,245 200,245 C 260,245 290,225 290,180 C 290,120 260,80 200,80 Z" 
                              fill="rgba(15, 23, 42, 0.015)" stroke="rgba(15, 23, 42, 0.1)" strokeWidth="1" 
                              transform={`translate(200, 150) scale(${ventricleScale}) translate(-200, -150)`} />
                            
                            <path d="M 200,120 Q 150,130 150,170 T 200,215 Q 250,210 250,170 T 200,120 Z" 
                              fill="none" stroke="rgba(15, 23, 42, 0.08)" strokeWidth="0.75" 
                              transform={`translate(200, 150) scale(${ventricleScale}) translate(-200, -150)`} />
                            
                            {/* Vector pinpoint marker dynamically sizing with slice selector */}
                            {lesionRadius > 0 && (
                              <g transform={`translate(${lesionX}, ${lesionY})`}>
                                {/* Micro pointer dot */}
                                <circle cx="0" cy="0" r={lesionRadius} fill="var(--accent)" />
                                <circle cx="0" cy="0" r={lesionRadius * 2.5} fill="none" stroke="var(--accent)" strokeWidth="0.75" strokeDasharray="2 1" />
                                {/* Vector indicator line pointing to label */}
                                <line x1="0" y1="0" x2="35" y2="-20" stroke="var(--accent)" strokeWidth="0.75" />
                                {/* Label container */}
                                <g transform="translate(35, -35)">
                                  <rect x="0" y="0" width="135" height="24" rx="2" fill="#ffffff" stroke="rgba(15,23,42,0.1)" strokeWidth="0.75" />
                                  <text x="8" y="10" fill="var(--accent)" fontSize="7.5" fontWeight="bold" fontFamily="monospace">PATHOLOGY FOCUS</text>
                                  <text x="8" y="18" fill="rgba(15,23,42,0.6)" fontSize="6.5" fontFamily="monospace">{`D: ${(lesionRadius * 0.4).toFixed(2)}cm | CONF: 96.42%`}</text>
                                </g>
                              </g>
                            )}
                          </svg>
                        </div>
                        
                        {/* Scan Telemetry HUD overlay info */}
                        <div className="scan-hud-telemetry">
                          <div>SEQUENCE: T2-FLAIR-SAG</div>
                          <div>TR: 4500ms | TE: 120ms</div>
                          <div>SLICE: {mriSlice} / 22 | FOV: 240mm</div>
                          <div>RESOLUTION: 512 x 512px</div>
                        </div>
                      </div>
                      
                      <div className="scan-findings-panel">
                        <h4 className="findings-title"><AlertCircle size={14} style={{ color: 'var(--accent)', marginRight: '0.35rem' }} /> CLINICAL FINDINGS</h4>
                        <p className="findings-desc clinical-text-font" style={{ fontSize: '0.95rem' }}>{activeReport.summary || "High resolution imaging sweep shows localized tissue inflammation consistent with autoimmune arthritic flare. Indicator vector points to focal synovial thickening in articulation joint."}</p>
                        
                        {/* Interactive Slice Controls */}
                        <div className="mri-slice-controls" style={{ margin: '1.15rem 0', background: 'rgba(15,23,42,0.015)', border: '1px solid rgba(15,23,42,0.03)', borderRadius: 'var(--radius-md)', padding: '0.85rem' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', color: 'var(--text-secondary)', fontFamily: 'monospace', marginBottom: '0.5rem', fontWeight: 600 }}>
                            <span>SCRUB MRI VOLUME</span>
                            <span className="text-accent" style={{ fontWeight: 'bold' }}>Slice {mriSlice} / 22</span>
                          </div>
                          <input
                            type="range"
                            min="1"
                            max="22"
                            value={mriSlice}
                            onChange={e => setMriSlice(parseInt(e.target.value))}
                            className="mri-slice-slider"
                            style={{ width: '100%', accentColor: 'var(--accent)', cursor: 'ew-resize', outline: 'none' }}
                          />
                        </div>

                        <div className="findings-telemetry-metrics">
                          <div className="finding-metric">
                            <span className="metric-label">LESION DIAMETER:</span>
                            <span className="metric-val text-warning">{(lesionRadius * 0.4).toFixed(2)} cm</span>
                          </div>
                          <div className="finding-metric">
                            <span className="metric-label">SURROUNDING EDEMA:</span>
                            <span className="metric-val text-secondary">{lesionRadius > 0 ? 'MODERATE (34cc)' : 'NONE'}</span>
                          </div>
                          <div className="finding-metric">
                            <span className="metric-label">DIAGNOSTIC CONFIDENCE:</span>
                            <span className="metric-val text-info">96.42%</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* LAB / METABOLIC REPORT PANEL */}
                  {activeReport.type === 'lab' && (
                    <div className="lab-visualizer-dock">
                      <div className="lab-data-table-panel">
                        <table className="lab-table">
                          <thead>
                            <tr>
                              <th>BIOMARKER</th>
                              <th>VALUE</th>
                              <th>REF. RANGE</th>
                              <th>STATUS</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr className={selectedBiomarker === 'PLT' ? 'selected-row' : ''} onClick={() => setSelectedBiomarker('PLT')} style={{ cursor: 'pointer' }}>
                              <td>Platelet Count (PLT)</td>
                              <td className="text-warning font-mono font-bold">92,000 / µL</td>
                              <td className="font-mono text-muted">150,000 - 450,000</td>
                              <td><span className="mini-badge bg-danger">LOW</span></td>
                            </tr>
                            <tr className={selectedBiomarker === 'WBC' ? 'selected-row' : ''} onClick={() => setSelectedBiomarker('WBC')} style={{ cursor: 'pointer' }}>
                              <td>White Blood Cell (WBC)</td>
                              <td className="text-warning font-mono font-bold">12.4 x10^3/µL</td>
                              <td className="font-mono text-muted">4.5 - 11.0</td>
                              <td><span className="mini-badge bg-warning">HIGH</span></td>
                            </tr>
                            <tr className={selectedBiomarker === 'CRP' ? 'selected-row' : ''} onClick={() => setSelectedBiomarker('CRP')} style={{ cursor: 'pointer' }}>
                              <td>C-Reactive Protein (CRP)</td>
                              <td className="text-warning font-mono font-bold">42.5 mg/L</td>
                              <td className="font-mono text-muted">&lt; 3.0</td>
                              <td><span className="mini-badge bg-danger">CRITICAL</span></td>
                            </tr>
                          </tbody>
                        </table>
                        
                        {/* Interactive Historical Graph for selected biomarker */}
                        <div className="historical-biomarker-chart" style={{ marginTop: '1rem', background: 'rgba(15,23,42,0.015)', border: '1px solid rgba(15,23,42,0.03)', borderRadius: 'var(--radius-md)', padding: '0.85rem' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', color: 'var(--text-secondary)', fontFamily: 'monospace', marginBottom: '0.45rem' }}>
                            <span>HISTORICAL PATH [30 DAYS]</span>
                            <span className="text-accent" style={{ fontWeight: 'bold' }}>{selectedBiomarkerHistory.name}</span>
                          </div>
                          <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', height: '65px', padding: '0.25rem 0.5rem 0' }}>
                            {selectedBiomarkerHistory.values.map((val, idx) => {
                              const maxVal = Math.max(...selectedBiomarkerHistory.values)
                              const heightPct = `${(val / maxVal) * 100}%`
                              return (
                                <div key={idx} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', flex: 1, height: '100%', justifyContent: 'flex-end' }}>
                                  <span style={{ fontSize: '0.65rem', fontFamily: 'monospace', color: 'var(--text-primary)', fontWeight: 'bold', marginBottom: '0.2rem' }}>{val}</span>
                                  <div style={{ width: '22px', height: heightPct, background: 'var(--accent)', opacity: 0.6 + idx * 0.12, borderRadius: '2px 2px 0 0', position: 'relative' }}>
                                    <div className="chart-bar-glow" />
                                  </div>
                                </div>
                              )
                            })}
                          </div>
                          <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.5rem', fontFamily: 'monospace', textAlign: 'center' }}>
                            {selectedBiomarkerHistory.desc}
                          </p>
                        </div>
                      </div>
                      
                      <div className="lab-ecg-sim-panel">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                          <h4 className="findings-title" style={{ margin: 0 }}><Activity size={14} style={{ color: 'var(--accent)', marginRight: '0.35rem' }} /> REALTIME HEART VITAL</h4>
                          <button className="action-btn text-accent" onClick={() => setHeartRate(r => r === 74 ? 120 : r === 120 ? 45 : 74)} title="Trigger heart rate change" style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.7rem', fontFamily: 'monospace', background: 'rgba(15,23,42,0.03)', padding: '0.15rem 0.4rem', borderRadius: '4px', border: '1px solid rgba(15,23,42,0.05)' }}>
                            <Heart size={10} className="heartbeat-pulse" /> {heartRate} BPM
                          </button>
                        </div>
                        <div className="ecg-graph-box">
                          {/* Dynamic ECG path matching heartRate state */}
                          <svg viewBox="0 0 350 80" className="ecg-svg">
                            <path 
                              d="M 0,40 L 40,40 L 50,20 L 60,60 L 70,40 L 110,40 L 120,40 L 125,5 L 132,75 L 140,40 L 155,48 L 165,40 L 210,40 L 220,20 L 230,60 L 240,40 L 280,40 L 290,40 L 295,5 L 302,75 L 310,40 L 325,48 L 335,40 L 350,40" 
                              fill="none" 
                              stroke="var(--accent)" 
                              strokeWidth="1.5" 
                              className="ecg-animated-path" 
                              style={{ animationDuration: heartRate === 120 ? '1s' : heartRate === 45 ? '2.5s' : '1.7s' }}
                            />
                          </svg>
                        </div>
                        <p className="clinical-text-font" style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.65rem', lineHeight: '1.5' }}>
                          <strong>Vitals telemetry check:</strong> Rhythm is {heartRate === 120 ? 'Tachycardic' : heartRate === 45 ? 'Bradycardic' : 'Normal Sinus'}. Heart rate average: {heartRate} BPM. Blood pressure: {heartRate === 120 ? '138/88' : heartRate === 45 ? '104/62' : '118/74'} mmHg.
                        </p>
                      </div>
                    </div>
                  )}

                  {/* GENETICS / DNA SEQUENCE VIEW */}
                  {activeReport.type === 'genetics' && (
                    <div className="genetics-visualizer-dock">
                      <div className="dna-strands-visualization-panel" style={{ position: 'relative', overflow: 'hidden' }}>
                        {/* Overlapping 3D rotating double helix wireframe */}
                        <svg viewBox="0 0 300 120" className="dna-sine-wave-svg" style={{ width: '100%', height: '140px', overflow: 'visible', zIndex: 2 }}>
                          <defs>
                            <linearGradient id="strandGlow1" x1="0%" y1="0%" x2="100%" y2="0%">
                              <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.8" />
                              <stop offset="100%" stopColor="var(--info)" stopOpacity="0.8" />
                            </linearGradient>
                            <linearGradient id="strandGlow2" x1="0%" y1="0%" x2="100%" y2="0%">
                              <stop offset="0%" stopColor="var(--info)" stopOpacity="0.4" />
                              <stop offset="100%" stopColor="var(--accent)" stopOpacity="0.4" />
                            </linearGradient>
                          </defs>
                          {/* Live rendered depth-sorted 3D nodes */}
                          {renderDnaStrands()}
                        </svg>
                        <span className="dna-helix-subtitle" style={{ zIndex: 2 }}>DYNAMIC 3D PERSPECTIVE CHROMOSOME 6 ALIGNMENT</span>
                      </div>
                      
                      <div className="genetics-findings-panel">
                        <h4 className="findings-title"><Dna size={14} style={{ color: 'var(--accent)', marginRight: '0.35rem' }} /> ALLELIC RISK SUSCEPTIBILITY</h4>
                        <div className="genetics-risk-card">
                          <div className="genetics-risk-title">HLA-DRB1 GENOTYPING</div>
                          <p className="clinical-text-font" style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', margin: '0.45rem 0' }}>
                            Patient carries heterozygous alleles: <strong>DRB1*03:01</strong> / <strong>DRB1*15:01</strong>.
                          </p>
                          <div className="risk-factor-bar-wrapper">
                            <div className="risk-factor-label">LUPUS SUSCEPTIBILITY MULTIPLIER:</div>
                            <div className="risk-value text-warning">4.21x Risk</div>
                          </div>
                          <div className="risk-gauge-bar">
                            <div className="risk-gauge-fill" style={{ width: '84%' }} />
                          </div>
                        </div>
                        <p className="clinical-text-font" style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.65rem', lineHeight: '1.4' }}>
                          HLA-DRB1*03:01 is associated with strong immune activation and elevated production of anti-dsDNA autoantibodies.
                        </p>
                      </div>
                    </div>
                  )}

                  {/* PRESCRIPTION FORM VIEW */}
                  {activeReport.type === 'prescription' && (
                    <div className="prescription-visualizer-dock" style={{ display: 'flex', justifyContent: 'center' }}>
                      <div className="prescription-futuristic-slip glassmorphic-panel">
                        <div className="rx-slip-header">
                          <div style={{ fontSize: '2.5rem', fontWeight: 900, color: 'var(--accent)', lineHeight: 1 }}>℞</div>
                          <div style={{ textAlign: 'right' }}>
                            <div style={{ fontSize: '0.8rem', fontWeight: 700 }}>RARESENSE CLINICAL DIRECT</div>
                            <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>RX-LIC: #RS-99482-B</div>
                          </div>
                        </div>
                        
                        <div className="rx-slip-body" style={{ margin: '1rem 0', borderTop: '1px dashed var(--border)', borderBottom: '1px dashed var(--border)', padding: '1rem 0' }}>
                          <div className="rx-drug-item">
                            <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 700, fontSize: '0.9rem' }}>
                              <span>Hydroxychloroquine Sulfate 200mg</span>
                              <span>#60 Tabs</span>
                            </div>
                            <div className="clinical-text-font" style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>Take 1 tablet by mouth twice daily with meals. Autoimmune modulator.</div>
                          </div>
                          <div className="rx-drug-item" style={{ marginTop: '1rem' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 700, fontSize: '0.9rem' }}>
                              <span>Prednisone 10mg</span>
                              <span>#30 Tabs</span>
                            </div>
                            <div className="clinical-text-font" style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>Take 1 tablet by mouth daily in morning. Corticosteroid flare control.</div>
                          </div>
                        </div>

                        <div className="rx-slip-footer" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                            <CheckCircle size={14} style={{ color: 'var(--success)' }} />
                            <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', fontFamily: 'monospace' }}>SECURE VERIFICATION HASH: 8f4d92a1</span>
                          </div>
                          <div style={{ borderTop: '1px solid var(--text-muted)', width: '120px', textAlign: 'center', paddingTop: '0.25rem' }}>
                            <span style={{ fontSize: '0.65rem', color: 'var(--text-tertiary)' }}>Digital Doctor Key</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                </div>

                {/* Footer Action Bar */}
                <div className="modal-footer" style={{ borderTop: '1px solid var(--border)', paddingTop: '0.85rem', marginTop: '1rem', display: 'flex', justifyContent: 'space-between' }}>
                  <button type="button" className="btn btn-secondary" onClick={() => {
                    alert("Simulating PDF download for: " + activeReport.file_name)
                  }} style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}>
                    <Download size={14} /> Download Document
                  </button>
                  <button type="button" className="btn btn-primary" onClick={() => { setShowReportViewer(false); setActiveReport(null); }}>
                    Close Preview
                  </button>
                </div>
              </div>
            )}
            
          </div>
        </div>
      )}

    </div>
  )
}
