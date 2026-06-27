import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../utils/api'
import { ArrowLeft, Plus, Play, Calendar, User, Droplet, FileText, Dna, AlertTriangle, CheckCircle, XCircle, Clock } from 'lucide-react'

export default function PatientDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [patient, setPatient] = useState(null)
  const [timeline, setTimeline] = useState(null)
  const [matches, setMatches] = useState([])
  const [tab, setTab] = useState('timeline')
  const [loading, setLoading] = useState(true)
  const [matching, setMatching] = useState(false)
  const [showNoteModal, setShowNoteModal] = useState(false)
  const [noteForm, setNoteForm] = useState({ note_type: 'consultation', specialty: 'General', physician: '', date: '', text: '' })

  useEffect(() => { loadPatient() }, [id])

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

  async function addNote(e) {
    e.preventDefault()
    try {
      await api.addNote(id, { ...noteForm, date: new Date(noteForm.date).toISOString() })
      setShowNoteModal(false)
      setNoteForm({ note_type: 'consultation', specialty: 'General', physician: '', date: '', text: '' })
      loadPatient()
    } catch (err) {
      alert(err.message)
    }
  }

  if (loading) return <div className="loading-container"><div className="spinner" /></div>
  if (!patient) return <div className="empty-state"><h3>Patient not found</h3></div>

  const age = patient.date_of_birth ? Math.floor((Date.now() - new Date(patient.date_of_birth)) / 31557600000) : '?'

  return (
    <div className="fade-in">
      {/* Back button */}
      <button className="btn btn-secondary btn-sm" onClick={() => navigate('/patients')} style={{ marginBottom: '1rem' }}>
        <ArrowLeft size={14} /> Back to Patients
      </button>

      {/* Patient Header */}
      <div className="patient-header-card">
        <div className="patient-avatar-lg">
          {patient.first_name?.[0]}{patient.last_name?.[0]}
        </div>
        <div style={{ flex: 1 }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700 }}>{patient.first_name} {patient.last_name}</h2>
          <div className="patient-meta">
            <div className="patient-meta-item"><User size={14} />{age} yrs, {patient.gender === 'F' ? 'Female' : patient.gender === 'M' ? 'Male' : patient.gender}</div>
            {patient.blood_type && <div className="patient-meta-item"><Droplet size={14} />{patient.blood_type}</div>}
            <div className="patient-meta-item"><FileText size={14} />{patient.notes_count || 0} Notes</div>
            <div className="patient-meta-item"><Dna size={14} />{matches.length} Matches</div>
            <div className="patient-meta-item"><Calendar size={14} />ID: {patient.patient_id}</div>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button className="btn btn-primary" onClick={runMatching} disabled={matching}>
            {matching ? <><span className="loading-dots"><span></span><span></span><span></span></span> Matching...</> : <><Play size={14} /> Run Matching</>}
          </button>
          <button className="btn btn-secondary" onClick={() => setShowNoteModal(true)}>
            <Plus size={14} /> Add Note
          </button>
        </div>
      </div>

      {/* Patient Info Cards */}
      <div className="grid-3" style={{ marginBottom: '1.5rem' }}>
        <div className="card">
          <h4 style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Medical History</h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem' }}>
            {(patient.medical_history || []).length > 0
              ? patient.medical_history.map((h, i) => <span key={i} className="badge badge-warning">{h}</span>)
              : <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>No history</span>}
          </div>
        </div>
        <div className="card">
          <h4 style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Current Medications</h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem' }}>
            {(patient.current_medications || []).length > 0
              ? patient.current_medications.map((m, i) => <span key={i} className="entity-tag medication">{m}</span>)
              : <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>None</span>}
          </div>
        </div>
        <div className="card">
          <h4 style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Allergies</h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem' }}>
            {(patient.allergies || []).length > 0
              ? patient.allergies.map((a, i) => <span key={i} className="badge badge-danger">{a}</span>)
              : <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>None known</span>}
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button className={`tab ${tab === 'timeline' ? 'active' : ''}`} onClick={() => setTab('timeline')}>Timeline ({timeline?.total_visits || 0})</button>
        <button className={`tab ${tab === 'matches' ? 'active' : ''}`} onClick={() => setTab('matches')}>Disease Matches ({matches.length})</button>
      </div>

      {/* Timeline Tab */}
      {tab === 'timeline' && (
        <div className="timeline">
          {timeline?.timeline?.length > 0 ? timeline.timeline.map((entry, i) => (
            <div key={i} className="timeline-item">
              <div className="timeline-date">
                <Calendar size={12} style={{ display: 'inline', marginRight: '0.35rem', verticalAlign: 'text-bottom' }} />
                {new Date(entry.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
                <span style={{ marginLeft: '0.75rem' }} className="badge badge-info">{entry.specialty}</span>
                <span style={{ marginLeft: '0.35rem' }} className="badge badge-accent">{entry.note_type?.replace(/_/g, ' ')}</span>
              </div>
              <div className="timeline-card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <h4>{entry.specialty} — {entry.note_type?.replace(/_/g, ' ')}</h4>
                  <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{entry.physician}</span>
                </div>
                <p>{entry.summary}...</p>
                
                {/* Extracted entities */}
                <div className="timeline-entities">
                  {entry.symptoms?.map((s, j) => (
                    <span key={j} className="entity-tag symptom" title={s.hpo_code}>
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
              </div>
            </div>
          )) : (
            <div className="empty-state">
              <FileText size={48} />
              <h3>No clinical notes yet</h3>
              <p>Add clinical notes to build the patient's health timeline</p>
              <button className="btn btn-primary" onClick={() => setShowNoteModal(true)} style={{ marginTop: '1rem' }}>
                <Plus size={14} /> Add First Note
              </button>
            </div>
          )}
        </div>
      )}

      {/* Matches Tab */}
      {tab === 'matches' && (
        <div>
          {matches.length > 0 ? matches.map((match, i) => {
            const confPct = Math.round(match.confidence * 100)
            const level = confPct >= 60 ? 'high' : confPct >= 30 ? 'medium' : 'low'
            return (
              <div key={i} className={`match-card ${level}`}>
                <div className="match-header">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flex: 1 }}>
                    <div className="match-rank">{match.rank}</div>
                    <div>
                      <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>{match.disease_name}</h3>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>{match.disease_orpha_id}</span>
                    </div>
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
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem', marginTop: '0.35rem' }}>
                  {match.matched_symptoms?.map((s, j) => (
                    <span key={j} className="entity-tag symptom">{s.symptom_name}</span>
                  ))}
                </div>
              </div>
            )
          }) : (
            <div className="empty-state">
              <Dna size={48} />
              <h3>No matches yet</h3>
              <p>Click "Run Matching" to analyze the patient's symptoms against the rare disease database</p>
              <button className="btn btn-primary" onClick={runMatching} disabled={matching} style={{ marginTop: '1rem' }}>
                <Play size={14} /> Run Matching Engine
              </button>
            </div>
          )}
        </div>
      )}

      {/* Add Note Modal */}
      {showNoteModal && (
        <div className="modal-overlay" onClick={() => setShowNoteModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()} style={{ maxWidth: '700px' }}>
            <div className="modal-header">
              <h2>Add Clinical Note</h2>
              <button className="modal-close" onClick={() => setShowNoteModal(false)}>✕</button>
            </div>
            <form onSubmit={addNote}>
              <div className="modal-body">
                <div className="grid-2">
                  <div className="form-group">
                    <label>Note Type</label>
                    <select className="form-select" value={noteForm.note_type} onChange={e => setNoteForm({ ...noteForm, note_type: e.target.value })}>
                      <option value="consultation">Consultation</option>
                      <option value="discharge_summary">Discharge Summary</option>
                      <option value="progress_note">Progress Note</option>
                      <option value="radiology">Radiology Report</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Specialty</label>
                    <select className="form-select" value={noteForm.specialty} onChange={e => setNoteForm({ ...noteForm, specialty: e.target.value })}>
                      {['General', 'Dermatology', 'Hematology', 'Nephrology', 'Primary Care', 'Rheumatology', 'Neurology', 'Cardiology', 'Pulmonology', 'Endocrinology', 'Gastroenterology', 'Immunology'].map(s => (
                        <option key={s} value={s}>{s}</option>
                      ))}
                    </select>
                  </div>
                </div>
                <div className="grid-2">
                  <div className="form-group">
                    <label>Physician</label>
                    <input className="form-input" placeholder="Dr. Smith" value={noteForm.physician} onChange={e => setNoteForm({ ...noteForm, physician: e.target.value })} />
                  </div>
                  <div className="form-group">
                    <label>Date</label>
                    <input className="form-input" type="date" required value={noteForm.date} onChange={e => setNoteForm({ ...noteForm, date: e.target.value })} />
                  </div>
                </div>
                <div className="form-group">
                  <label>Clinical Note Text</label>
                  <textarea
                    className="form-textarea"
                    rows={8}
                    required
                    placeholder="Enter clinical note text... (e.g., Patient presents with erythematous malar rash across both cheeks. Reports photosensitivity...)"
                    value={noteForm.text}
                    onChange={e => setNoteForm({ ...noteForm, text: e.target.value })}
                  />
                  <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.25rem', display: 'block' }}>
                    The NLP engine will automatically extract symptoms, medications, diagnoses, and lab values from the text.
                  </span>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowNoteModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary"><Plus size={14} /> Add Note</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
