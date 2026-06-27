import { useState, useEffect, useRef } from 'react'
import { api } from '../utils/api'
import { Activity, Upload, Edit2, Check, X, FileText, BrainCircuit, Trash2, Calendar, User } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function PatientDashboard() {
  const [profile, setProfile] = useState(null)
  const [timeline, setTimeline] = useState([])
  const [matches, setMatches] = useState(null)
  const [loading, setLoading] = useState(true)
  
  const [uploading, setUploading] = useState(false)
  const [editingNote, setEditingNote] = useState(null)
  const [editForm, setEditForm] = useState({ text: '', physician: '' })
  
  const [matching, setMatching] = useState(false)
  const fileInputRef = useRef(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    try {
      const p = await api.getMyPatientProfile()
      setProfile(p)
      if (p.patient_id) {
        const t = await api.getTimeline(p.patient_id)
        setTimeline(t.timeline || [])
        if (p.matches_count > 0) {
          const m = await api.getMatchResults(p.patient_id)
          setMatches(m)
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
    } catch (err) {
      alert("Failed to upload prescription")
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
    } catch (err) {
      alert("Failed to save changes")
    }
  }

  const deleteNote = async (noteId) => {
    if (!confirm("Are you sure you want to delete this record?")) return
    try {
      await api.deleteClinicalNote(noteId)
      await loadData()
    } catch (err) {
      alert("Failed to delete record")
    }
  }

  const runRecommendation = async () => {
    if (!profile) return
    setMatching(true)
    try {
      await api.runMatching(profile.patient_id, 3)
      await loadData()
    } catch (err) {
      alert("Failed to get recommendation")
    } finally {
      setMatching(false)
    }
  }

  if (loading) {
    return <div className="loading-container"><div className="spinner" /></div>
  }

  if (!profile) {
    return <div className="card">Error loading profile.</div>
  }

  return (
    <div className="dashboard-layout" style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <header className="dashboard-header">
        <div>
          <h2>My Health Portal</h2>
          <p>Welcome back, {profile.first_name} {profile.last_name}</p>
        </div>
        <button 
          className="btn btn-primary" 
          onClick={runRecommendation}
          disabled={matching || timeline.length === 0}
        >
          {matching ? <><span className="spinner" style={{ width: 14, height: 14, borderWidth: 2 }} /> Analyzing...</> : <><BrainCircuit size={18} /> Get AI Recommendation</>}
        </button>
      </header>

      <div className="dashboard-grid">
        <div className="card" style={{ gridColumn: '1 / -1' }}>
          <div className="card-header">
            <h3><Upload size={18} /> Upload Clinical Document</h3>
          </div>
          <div 
            className="upload-area" 
            style={{ 
              border: '2px dashed var(--border-color)', 
              borderRadius: 'var(--radius-md)', 
              padding: '2rem', 
              textAlign: 'center',
              cursor: 'pointer',
              background: 'var(--bg-elevated)'
            }}
            onClick={() => fileInputRef.current?.click()}
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
                <div className="spinner"></div>
                <p>Running OCR extraction on document...</p>
              </div>
            ) : (
              <>
                <FileText size={32} style={{ color: 'var(--text-tertiary)', marginBottom: '1rem' }} />
                <h4>Click or drag to upload a prescription or clinical note</h4>
                <p style={{ color: 'var(--text-tertiary)', fontSize: '0.85rem' }}>Supports JPG, PNG, PDF</p>
              </>
            )}
          </div>
        </div>

        {matches && matches.matches && matches.matches.length > 0 && (
          <div className="card" style={{ gridColumn: '1 / -1', borderLeft: '4px solid var(--accent-light)' }}>
            <div className="card-header">
              <h3><BrainCircuit size={18} /> AI Recommendation</h3>
            </div>
            <div style={{ padding: '1rem', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-sm)' }}>
              <p style={{ marginBottom: '1rem', color: 'var(--text-secondary)' }}>Based on your clinical timeline, the AI engine has found potential matches for your symptoms. Please consult a doctor for official diagnosis.</p>
              
              <div style={{ display: 'grid', gap: '1rem' }}>
                {matches.matches.slice(0, 3).map((match, idx) => (
                  <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)' }}>
                    <div>
                      <h4 style={{ color: 'var(--accent-light)', marginBottom: '0.25rem' }}>{match.disease.name}</h4>
                      <p style={{ fontSize: '0.85rem', color: 'var(--text-tertiary)' }}>{match.matched_symptoms.length} matching symptoms found in your timeline</p>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '1.25rem', fontWeight: 600 }}>{(match.probability * 100).toFixed(1)}%</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>Match Probability</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="card" style={{ gridColumn: '1 / -1' }}>
          <div className="card-header">
            <h3><Activity size={18} /> Clinical Timeline</h3>
          </div>
          
          {timeline.length === 0 ? (
            <p style={{ color: 'var(--text-tertiary)', textAlign: 'center', padding: '2rem 0' }}>No clinical notes uploaded yet.</p>
          ) : (
            <div className="timeline-container" style={{ padding: '1rem 0' }}>
              {timeline.map((note) => (
                <div key={note.note_id} style={{ 
                  display: 'flex', 
                  gap: '1rem', 
                  paddingBottom: '2rem', 
                  borderLeft: '2px solid var(--border-color)',
                  marginLeft: '1rem',
                  paddingLeft: '1.5rem',
                  position: 'relative'
                }}>
                  <div style={{
                    position: 'absolute',
                    left: '-0.45rem',
                    top: 0,
                    width: '0.75rem',
                    height: '0.75rem',
                    borderRadius: '50%',
                    background: 'var(--accent-light)',
                    boxShadow: '0 0 0 4px var(--bg-primary)'
                  }} />
                  
                  <div style={{ flex: 1 }}>
                    {editingNote === note.note_id ? (
                      <div style={{ background: 'var(--bg-elevated)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
                        <div className="form-group">
                          <label>Doctor / Physician</label>
                          <input 
                            className="form-input" 
                            value={editForm.physician} 
                            onChange={e => setEditForm({...editForm, physician: e.target.value})}
                          />
                        </div>
                        <div className="form-group" style={{ marginTop: '1rem' }}>
                          <label>Clinical Notes</label>
                          <textarea 
                            className="form-input" 
                            rows={4}
                            value={editForm.text} 
                            onChange={e => setEditForm({...editForm, text: e.target.value})}
                          />
                        </div>
                        <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
                          <button className="btn btn-primary btn-sm" onClick={() => saveEdit(note.note_id)}>Save</button>
                          <button className="btn btn-secondary btn-sm" onClick={() => setEditingNote(null)}>Cancel</button>
                        </div>
                      </div>
                    ) : (
                      <div style={{ background: 'var(--bg-elevated)', padding: '1.25rem', borderRadius: 'var(--radius-md)', position: 'relative' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                            <span style={{ fontSize: '0.85rem', color: 'var(--text-tertiary)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                              <Calendar size={14} /> {new Date(note.date).toLocaleDateString()}
                            </span>
                            <span style={{ fontSize: '0.85rem', color: 'var(--text-tertiary)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                              <User size={14} /> {note.physician || 'Unknown Doctor'}
                            </span>
                          </div>
                          <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <button className="btn-icon" onClick={() => startEdit(note)} title="Edit record"><Edit2 size={16} /></button>
                            <button className="btn-icon" onClick={() => deleteNote(note.note_id)} title="Delete record"><Trash2 size={16} style={{ color: 'var(--danger)' }} /></button>
                          </div>
                        </div>
                        <p style={{ color: 'var(--text-secondary)', lineHeight: 1.6 }}>{note.summary}</p>
                        
                        {note.symptoms && note.symptoms.length > 0 && (
                          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '1rem' }}>
                            {note.symptoms.map((s, idx) => (
                              <span key={idx} className="badge badge-warning" style={{ fontSize: '0.7rem' }}>{s.normalized_name}</span>
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
    </div>
  )
}
