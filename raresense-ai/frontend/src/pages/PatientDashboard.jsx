import { useState, useEffect, useRef } from 'react'
import { api } from '../utils/api'
import {
  Upload, FileText, Calendar, User, Activity,
  Pill, FlaskConical, Thermometer, HeartPulse,
  CheckCircle, ClipboardList, Trash2, Edit2, Check, X
} from 'lucide-react'

export default function PatientDashboard() {
  const [profile, setProfile] = useState(null)
  const [timeline, setTimeline] = useState([])
  const [approvedDiagnoses, setApprovedDiagnoses] = useState([])
  const [loading, setLoading] = useState(true)

  const [uploading, setUploading] = useState(false)
  const [editingNote, setEditingNote] = useState(null)
  const [editForm, setEditForm] = useState({ text: '', physician: '' })

  const fileInputRef = useRef(null)

  useEffect(() => { loadData() }, [])

  const loadData = async () => {
    setLoading(true)
    try {
      const p = await api.getMyPatientProfile()
      setProfile(p)
      if (p.patient_id) {
        const t = await api.getTimeline(p.patient_id)
        setTimeline(t.timeline || [])

        // Load only clinician-approved matches
        try {
          const m = await api.getMatchResults(p.patient_id)
          const approved = (m.matches || []).filter(
            match => match.status === 'confirmed' || match.status === 'approved'
          )
          setApprovedDiagnoses(approved)
        } catch {
          setApprovedDiagnoses([])
        }
      }
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)
      await api.uploadPrescription(formData)
      await loadData()
    } catch {
      alert('Failed to upload prescription')
    } finally {
      setUploading(false)
      if (fileInputRef.current) fileInputRef.current.value = ''
    }
  }

  const startEdit = (note) => {
    setEditingNote(note.note_id)
    setEditForm({ text: note.summary, physician: note.physician })
  }

  const saveEdit = async (noteId) => {
    try {
      await api.updateClinicalNote(noteId, editForm)
      setEditingNote(null)
      await loadData()
    } catch {
      alert('Failed to save changes')
    }
  }

  const deleteNote = async (noteId) => {
    if (!confirm('Are you sure you want to delete this record?')) return
    try {
      await api.deleteClinicalNote(noteId)
      await loadData()
    } catch {
      alert('Failed to delete record')
    }
  }

  // Compute aggregated stats from timeline (pure math — no AI)
  const computeStats = () => {
    let totalSymptoms = 0
    let totalMedications = 0
    let totalLabValues = 0
    let visitCount = timeline.length

    for (const note of timeline) {
      totalSymptoms += (note.symptoms || []).length
      totalMedications += (note.medications || []).length
      totalLabValues += (note.lab_values || []).length
    }

    // Collect unique medications across all notes
    const allMeds = []
    const seen = new Set()
    for (const note of timeline) {
      for (const m of (note.medications || [])) {
        const key = m.normalized_name?.toLowerCase()
        if (key && !seen.has(key)) {
          seen.add(key)
          allMeds.push(m.normalized_name)
        }
      }
    }

    // Abnormal lab reports from attached reports
    const abnormalReports = []
    for (const note of timeline) {
      for (const rep of (note.reports || [])) {
        if (rep.status === 'abnormal' || rep.status === 'critical') {
          abnormalReports.push(rep)
        }
      }
    }

    return { visitCount, totalSymptoms, totalMedications, totalLabValues, allMeds, abnormalReports }
  }

  if (loading) return <div className="loading-container"><div className="spinner" /></div>
  if (!profile) return <div className="card">Error loading profile.</div>

  const stats = computeStats()

  return (
    <div style={{ maxWidth: '1050px', margin: '0 auto' }}>
      {/* Header */}
      <div className="patient-header-card glassmorphic-panel" style={{ marginBottom: '1.75rem' }}>
        <div className="patient-avatar-lg glowing-avatar-border">
          {profile.first_name?.[0]}{profile.last_name?.[0]}
        </div>
        <div style={{ flex: 1 }}>
          <h2 style={{ fontSize: '1.65rem', fontWeight: 800, color: 'var(--text-primary)' }}>
            {profile.first_name} {profile.last_name}
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.25rem' }}>
            My Health Portal — Personal Clinical Record
          </p>
        </div>
        <div style={{ textAlign: 'right', fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'monospace' }}>
          <div>ID: {profile.patient_id}</div>
          <div style={{ marginTop: '0.25rem' }}>{profile.blood_type && `Blood: ${profile.blood_type}`}</div>
        </div>
      </div>

      {/* Stats Row — mathematical summary only */}
      <div className="grid-3" style={{ marginBottom: '1.75rem', gap: '1rem' }}>
        <div className="card glassmorphic-panel hover-card-rise" style={{ textAlign: 'center', padding: '1.25rem' }}>
          <ClipboardList size={28} style={{ color: 'var(--accent)', marginBottom: '0.5rem' }} />
          <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)' }}>{stats.visitCount}</div>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Clinical Visits</div>
        </div>
        <div className="card glassmorphic-panel hover-card-rise" style={{ textAlign: 'center', padding: '1.25rem' }}>
          <Thermometer size={28} style={{ color: 'var(--warning)', marginBottom: '0.5rem' }} />
          <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)' }}>{stats.totalSymptoms}</div>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Recorded Symptoms</div>
        </div>
        <div className="card glassmorphic-panel hover-card-rise" style={{ textAlign: 'center', padding: '1.25rem' }}>
          <FlaskConical size={28} style={{ color: 'var(--info)', marginBottom: '0.5rem' }} />
          <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)' }}>{stats.totalLabValues}</div>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Lab Values Recorded</div>
        </div>
      </div>

      {/* Clinician-Approved Diagnoses — only shown if clinician has approved */}
      {approvedDiagnoses.length > 0 && (
        <div className="card glassmorphic-panel" style={{
          marginBottom: '1.75rem',
          borderLeft: '4px solid var(--success)',
          background: 'linear-gradient(135deg, rgba(16,185,129,0.03), transparent)'
        }}>
          <div className="card-header" style={{ marginBottom: '1rem' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-primary)' }}>
              <CheckCircle size={18} style={{ color: 'var(--success)' }} />
              Clinician-Approved Diagnoses
            </h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
              The following diagnoses have been reviewed and confirmed by your treating physician.
            </p>
          </div>
          <div style={{ display: 'grid', gap: '0.75rem' }}>
            {approvedDiagnoses.map((match, idx) => {
              const confPct = Math.round((match.confidence || 0) * 100)
              return (
                <div key={idx} style={{
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  padding: '1rem 1.25rem',
                  background: 'rgba(16,185,129,0.04)',
                  border: '1px solid rgba(16,185,129,0.15)',
                  borderRadius: 'var(--radius-md)'
                }}>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-primary)' }}>
                      {match.disease_name}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.2rem', fontFamily: 'monospace' }}>
                      {match.disease_orpha_id} · Physician-confirmed
                    </div>
                    {match.matched_symptoms?.length > 0 && (
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem', marginTop: '0.5rem' }}>
                        {match.matched_symptoms.slice(0, 4).map((s, j) => (
                          <span key={j} className="entity-tag symptom" style={{ fontSize: '0.65rem' }}>
                            {s.symptom_name}
                          </span>
                        ))}
                        {match.matched_symptoms.length > 4 && (
                          <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', padding: '0.15rem 0.35rem' }}>
                            +{match.matched_symptoms.length - 4} more
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                  <div style={{ textAlign: 'right', flexShrink: 0, marginLeft: '1rem' }}>
                    <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--success)' }}>{confPct}%</div>
                    <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>match score</div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Current Medications — extracted from clinical notes */}
      {stats.allMeds.length > 0 && (
        <div className="card glassmorphic-panel" style={{ marginBottom: '1.75rem' }}>
          <div className="card-header" style={{ marginBottom: '0.85rem' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Pill size={18} style={{ color: 'var(--accent)' }} /> Current Medications
            </h3>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.45rem' }}>
            {stats.allMeds.map((med, i) => (
              <span key={i} className="entity-tag medication">{med}</span>
            ))}
          </div>
        </div>
      )}

      {/* Abnormal Reports Alert */}
      {stats.abnormalReports.length > 0 && (
        <div className="card glassmorphic-panel" style={{
          marginBottom: '1.75rem',
          borderLeft: '4px solid var(--warning)'
        }}>
          <div className="card-header" style={{ marginBottom: '0.85rem' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--warning)' }}>
              <HeartPulse size={18} /> Reports Requiring Attention
            </h3>
          </div>
          <div style={{ display: 'grid', gap: '0.5rem' }}>
            {stats.abnormalReports.map((rep, i) => (
              <div key={i} style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                padding: '0.65rem 0.85rem',
                background: rep.status === 'critical' ? 'rgba(239,68,68,0.05)' : 'rgba(245,158,11,0.05)',
                border: `1px solid ${rep.status === 'critical' ? 'rgba(239,68,68,0.15)' : 'rgba(245,158,11,0.12)'}`,
                borderRadius: 'var(--radius-sm)'
              }}>
                <div>
                  <div style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-primary)' }}>{rep.name}</div>
                  {rep.summary && (
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.15rem' }}>{rep.summary}</div>
                  )}
                </div>
                <span className={`badge ${rep.status === 'critical' ? 'badge-danger' : 'badge-warning'}`} style={{ flexShrink: 0, marginLeft: '1rem', fontSize: '0.65rem' }}>
                  {rep.status.toUpperCase()}
                </span>
              </div>
            ))}
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.85rem' }}>
            Please consult your treating physician regarding the above reports.
          </p>
        </div>
      )}

      {/* Upload Clinical Document */}
      <div className="card glassmorphic-panel" style={{ marginBottom: '1.75rem' }}>
        <div className="card-header" style={{ marginBottom: '0.85rem' }}>
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Upload size={18} style={{ color: 'var(--accent)' }} /> Upload Clinical Document
          </h3>
        </div>
        <div
          style={{
            border: '2px dashed var(--border)',
            borderRadius: 'var(--radius-md)',
            padding: '2rem',
            textAlign: 'center',
            cursor: 'pointer',
            background: 'rgba(15,23,42,0.015)',
            transition: 'border-color 0.2s ease'
          }}
          onClick={() => fileInputRef.current?.click()}
          onMouseEnter={e => e.currentTarget.style.borderColor = 'var(--accent)'}
          onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border)'}
        >
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handleFileUpload}
            accept="image/*,.pdf"
          />
          {uploading ? (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
              <div className="spinner" />
              <p style={{ color: 'var(--text-secondary)' }}>Running OCR extraction on document...</p>
            </div>
          ) : (
            <>
              <FileText size={32} style={{ color: 'var(--text-tertiary)', marginBottom: '0.75rem' }} />
              <h4 style={{ color: 'var(--text-primary)', marginBottom: '0.35rem' }}>Click to upload a prescription or clinical note</h4>
              <p style={{ color: 'var(--text-tertiary)', fontSize: '0.82rem' }}>Supports JPG, PNG, PDF</p>
            </>
          )}
        </div>
      </div>

      {/* Clinical Timeline */}
      <div className="card glassmorphic-panel">
        <div className="card-header" style={{ marginBottom: '1.25rem' }}>
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Activity size={18} style={{ color: 'var(--accent)' }} /> Clinical Timeline
          </h3>
        </div>

        {timeline.length === 0 ? (
          <p style={{ color: 'var(--text-tertiary)', textAlign: 'center', padding: '2rem 0', fontSize: '0.85rem' }}>
            No clinical notes on record yet.
          </p>
        ) : (
          <div className="timeline-container" style={{ padding: '0.5rem 0' }}>
            {timeline.map((note) => (
              <div
                key={note.note_id}
                style={{
                  display: 'flex',
                  gap: '1rem',
                  paddingBottom: '2rem',
                  borderLeft: '2px solid var(--border)',
                  marginLeft: '1rem',
                  paddingLeft: '1.5rem',
                  position: 'relative'
                }}
              >
                {/* Timeline dot */}
                <div style={{
                  position: 'absolute', left: '-0.45rem', top: 0,
                  width: '0.75rem', height: '0.75rem', borderRadius: '50%',
                  background: 'var(--accent)', boxShadow: '0 0 0 3px rgba(99,102,241,0.15)'
                }} />

                <div style={{ flex: 1 }}>
                  {editingNote === note.note_id ? (
                    <div className="glassmorphic-panel" style={{ padding: '1rem', borderRadius: 'var(--radius-md)' }}>
                      <div className="form-group">
                        <label>Doctor / Physician</label>
                        <input
                          className="form-input"
                          value={editForm.physician}
                          onChange={e => setEditForm({ ...editForm, physician: e.target.value })}
                        />
                      </div>
                      <div className="form-group" style={{ marginTop: '0.75rem' }}>
                        <label>Clinical Notes</label>
                        <textarea
                          className="form-textarea"
                          rows={4}
                          value={editForm.text}
                          onChange={e => setEditForm({ ...editForm, text: e.target.value })}
                        />
                      </div>
                      <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.75rem' }}>
                        <button className="btn btn-primary btn-sm" onClick={() => saveEdit(note.note_id)}>
                          <Check size={13} /> Save
                        </button>
                        <button className="btn btn-secondary btn-sm" onClick={() => setEditingNote(null)}>
                          <X size={13} /> Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="glassmorphic-panel hover-glow-border" style={{ padding: '1.1rem 1.25rem', borderRadius: 'var(--radius-md)' }}>
                      {/* Header row */}
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.65rem' }}>
                        <div style={{ display: 'flex', gap: '0.85rem', alignItems: 'center', flexWrap: 'wrap' }}>
                          <span style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                            <Calendar size={13} /> {new Date(note.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
                          </span>
                          <span style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                            <User size={13} /> {note.physician || 'Physician'}
                          </span>
                          {note.specialty && (
                            <span className="badge badge-info" style={{ fontSize: '0.65rem' }}>{note.specialty}</span>
                          )}
                        </div>
                        <div style={{ display: 'flex', gap: '0.4rem' }}>
                          <button className="action-btn text-info" onClick={() => startEdit(note)} title="Edit record">
                            <Edit2 size={14} />
                          </button>
                          <button className="action-btn text-danger" onClick={() => deleteNote(note.note_id)} title="Delete record">
                            <Trash2 size={14} />
                          </button>
                        </div>
                      </div>

                      {/* Note text */}
                      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.65, fontSize: '0.88rem', marginBottom: '0.65rem' }}>
                        {note.summary}
                      </p>

                      {/* Extracted symptoms (mathematical record — no AI label) */}
                      {note.symptoms?.length > 0 && (
                        <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap', marginBottom: '0.45rem' }}>
                          {note.symptoms.map((s, idx) => (
                            <span key={idx} className="entity-tag symptom" style={{ fontSize: '0.7rem' }}>
                              {s.normalized_name}
                            </span>
                          ))}
                        </div>
                      )}

                      {/* Medications */}
                      {note.medications?.length > 0 && (
                        <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap', marginBottom: '0.45rem' }}>
                          {note.medications.map((m, idx) => (
                            <span key={idx} className="entity-tag medication" style={{ fontSize: '0.7rem' }}>
                              {m.normalized_name}
                            </span>
                          ))}
                        </div>
                      )}

                      {/* Lab Values */}
                      {note.lab_values?.length > 0 && (
                        <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                          {note.lab_values.map((l, idx) => (
                            <span key={idx} className="entity-tag lab_value" style={{ fontSize: '0.7rem' }}>
                              {l.normalized_name}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
