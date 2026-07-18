import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../utils/api'
import { Plus, Search, Trash2, Eye, ChevronLeft, ChevronRight, UserPlus, Sliders } from 'lucide-react'

export default function Patients() {
  const [patients, setPatients] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [form, setForm] = useState({ first_name: '', last_name: '', date_of_birth: '', gender: 'M', blood_type: '', ethnicity: '', status: 'active', template: '' })
  const navigate = useNavigate()

  useEffect(() => { loadPatients() }, [page])

  async function loadPatients() {
    setLoading(true)
    try {
      const params = `?page=${page}&limit=15${search ? `&search=${search}` : ''}`
      const data = await api.getPatients(params)
      setPatients(data.patients || [])
      setTotal(data.total || 0)
      setPages(data.pages || 1)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  function handleTemplateChange(e) {
    const val = e.target.value
    let autoData = { template: val }
    if (val === 'lupus') {
      autoData = { ...autoData, first_name: 'Elena', last_name: 'Vasquez', date_of_birth: '1998-05-14', gender: 'F', blood_type: 'O+', ethnicity: 'Hispanic' }
    } else if (val === 'cystic_fibrosis') {
      autoData = { ...autoData, first_name: 'Liam', last_name: 'Miller', date_of_birth: '2024-02-10', gender: 'M', blood_type: 'A+', ethnicity: 'Caucasian' }
    } else if (val === 'huntington') {
      autoData = { ...autoData, first_name: 'Robert', last_name: 'Chen', date_of_birth: '1981-11-23', gender: 'M', blood_type: 'B-', ethnicity: 'Asian' }
    } else {
      autoData = { ...autoData, first_name: '', last_name: '', date_of_birth: '', gender: 'M', blood_type: '', ethnicity: '' }
    }
    setForm(prev => ({ ...prev, ...autoData }))
  }

  async function handleCreate(e) {
    e.preventDefault()
    try {
      await api.createPatient({ ...form, date_of_birth: new Date(form.date_of_birth).toISOString() })
      setShowModal(false)
      setForm({ first_name: '', last_name: '', date_of_birth: '', gender: 'M', blood_type: '', ethnicity: '', status: 'active', template: '' })
      loadPatients()
    } catch (err) {
      alert(err.message)
    }
  }

  async function handleDelete(patientId) {
    if (!confirm('Delete this patient and all associated data?')) return
    try {
      await api.deletePatient(patientId)
      loadPatients()
    } catch (err) {
      alert(err.message)
    }
  }

  function handleSearch(e) {
    e.preventDefault()
    setPage(1)
    loadPatients()
  }

  return (
    <div className="fade-in workspace-glow-bg">
      <div className="page-header">
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)' }}>Patients</h1>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-tertiary)' }}>{total} registered clinical profiles</p>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <form onSubmit={handleSearch} className="search-bar">
            <Search />
            <input
              placeholder="Search by name or disease..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              style={{ border: '1px solid rgba(255,255,255,0.04)', borderRadius: 'var(--radius-sm)' }}
            />
          </form>
          <button className="btn btn-primary btn-glow" onClick={() => setShowModal(true)}>
            <Plus size={15} /> Add Patient
          </button>
        </div>
      </div>

      {/* Patient Table */}
      <div className="table-container glassmorphic-panel">
        <table>
          <thead>
            <tr>
              <th>Patient ID</th>
              <th>Full Name</th>
              <th>Gender</th>
              <th>Date of Birth</th>
              <th>Blood</th>
              <th>Status</th>
              <th>Records</th>
              <th>Matches</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="9" style={{ textAlign: 'center', padding: '3.5rem' }}>
                  <div className="spinner" style={{ margin: '0 auto' }} />
                </td>
              </tr>
            ) : patients.length === 0 ? (
              <tr>
                <td colSpan="9" style={{ textAlign: 'center', padding: '3.5rem', color: 'var(--text-tertiary)' }}>
                  No clinical files found in directory
                </td>
              </tr>
            ) : patients.map(p => (
              <tr key={p.patient_id} onClick={() => navigate(`/patients/${p.patient_id}`)} style={{ transition: 'background 150ms' }}>
                <td>
                  <code className="patient-id-badge">{p.patient_id}</code>
                </td>
                <td style={{ color: 'var(--text-primary)', fontWeight: 700, fontSize: '0.92rem' }}>
                  {p.first_name} {p.last_name}
                </td>
                <td>
                  <span className="gender-dot-cell">
                    <span className={`gender-dot ${p.gender === 'F' ? 'female' : 'male'}`}></span>
                    {p.gender === 'F' ? 'Female' : p.gender === 'M' ? 'Male' : p.gender}
                  </span>
                </td>
                <td>{p.date_of_birth ? new Date(p.date_of_birth).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) : '-'}</td>
                <td style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>{p.blood_type || '-'}</td>
                <td>
                  <span className={`status-pill ${p.status === 'active' ? 'active' : 'discharged'}`}>
                    <span className="status-dot"></span>
                    {p.status}
                  </span>
                </td>
                <td style={{ fontWeight: 700, color: 'var(--info)' }}>{p.notes_count || 0}</td>
                <td style={{ fontWeight: 700, color: 'var(--accent-light)' }}>{p.matches_count || 0}</td>
                <td>
                  <div style={{ display: 'flex', gap: '0.5rem' }} onClick={e => e.stopPropagation()}>
                    <button className="action-btn text-info" onClick={() => navigate(`/patients/${p.patient_id}`)} title="Inspect timeline">
                      <Eye size={15} />
                    </button>
                    <button className="action-btn text-danger" onClick={() => handleDelete(p.patient_id)} title="Delete file">
                      <Trash2 size={15} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {pages > 1 && (
        <div className="pagination" style={{ marginTop: '1.5rem' }}>
          <button disabled={page <= 1} onClick={() => setPage(p => p - 1)}>
            <ChevronLeft size={13} />
          </button>
          {Array.from({ length: Math.min(pages, 7) }, (_, i) => i + 1).map(p => (
            <button key={p} className={page === p ? 'active' : ''} onClick={() => setPage(p)}>
              {p}
            </button>
          ))}
          <button disabled={page >= pages} onClick={() => setPage(p => p + 1)}>
            <ChevronRight size={13} />
          </button>
        </div>
      )}

      {/* Create Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal glassmorphic-panel slide-up-modal" onClick={e => e.stopPropagation()} style={{ maxWidth: '600px', width: '90%' }}>
            <div className="modal-header">
              <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><UserPlus size={18} style={{ color: 'var(--accent)' }} /> Add Patient File</h2>
              <button className="modal-close" onClick={() => setShowModal(false)}>✕</button>
            </div>
            <form onSubmit={handleCreate}>
              <div className="modal-body">
                <div className="form-group" style={{ marginBottom: '1.25rem' }}>
                  <label style={{ fontWeight: 650 }}>Clinical Case Template (Optional)</label>
                  <select 
                    className="form-select" 
                    value={form.template} 
                    onChange={handleTemplateChange}
                    style={{ border: '1px solid var(--border)', background: 'var(--bg-elevated)', cursor: 'pointer' }}
                  >
                    <option value="">None (Empty Profile)</option>
                    <option value="lupus">Lupus Study (Elena Vasquez)</option>
                    <option value="cystic_fibrosis">Cystic Fibrosis Case Template</option>
                    <option value="huntington">Huntington's Disease Case Template</option>
                  </select>
                </div>

                <div className="grid-2">
                  <div className="form-group">
                    <label>First Name</label>
                    <input className="form-input" required placeholder="Jane" value={form.first_name} onChange={e => setForm({ ...form, first_name: e.target.value })} />
                  </div>
                  <div className="form-group">
                    <label>Last Name</label>
                    <input className="form-input" required placeholder="Doe" value={form.last_name} onChange={e => setForm({ ...form, last_name: e.target.value })} />
                  </div>
                </div>
                <div className="grid-2">
                  <div className="form-group">
                    <label>Date of Birth</label>
                    <input className="form-input" type="date" required value={form.date_of_birth} onChange={e => setForm({ ...form, date_of_birth: e.target.value })} />
                  </div>
                  <div className="form-group">
                    <label>Biological Gender</label>
                    <select className="form-select" value={form.gender} onChange={e => setForm({ ...form, gender: e.target.value })}>
                      <option value="M">Male</option>
                      <option value="F">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>
                <div className="grid-2">
                  <div className="form-group">
                    <label>Blood Type</label>
                    <select className="form-select" value={form.blood_type} onChange={e => setForm({ ...form, blood_type: e.target.value })}>
                      <option value="">Select blood type</option>
                      {['A+','A-','B+','B-','AB+','AB-','O+','O-'].map(bt => <option key={bt} value={bt}>{bt}</option>)}
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Ethnicity</label>
                    <input className="form-input" placeholder="e.g. Hispanic" value={form.ethnicity} onChange={e => setForm({ ...form, ethnicity: e.target.value })} />
                  </div>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary btn-glow"><Plus size={14} /> Add Patient</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
