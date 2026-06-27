import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../utils/api'
import { Plus, Search, Trash2, Edit, Eye, ChevronLeft, ChevronRight } from 'lucide-react'

export default function Patients() {
  const [patients, setPatients] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [form, setForm] = useState({ first_name: '', last_name: '', date_of_birth: '', gender: 'M', blood_type: '', ethnicity: '', status: 'active' })
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

  async function handleCreate(e) {
    e.preventDefault()
    try {
      await api.createPatient({ ...form, date_of_birth: new Date(form.date_of_birth).toISOString() })
      setShowModal(false)
      setForm({ first_name: '', last_name: '', date_of_birth: '', gender: 'M', blood_type: '', ethnicity: '', status: 'active' })
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
    <div className="fade-in">
      <div className="page-header">
        <div>
          <h1>Patients</h1>
          <p>{total} patients in database</p>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <form onSubmit={handleSearch} className="search-bar">
            <Search />
            <input
              placeholder="Search patients..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
          </form>
          <button className="btn btn-primary" onClick={() => setShowModal(true)}>
            <Plus size={16} /> Add Patient
          </button>
        </div>
      </div>

      {/* Patient Table */}
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Patient ID</th>
              <th>Name</th>
              <th>Gender</th>
              <th>DOB</th>
              <th>Blood</th>
              <th>Status</th>
              <th>Notes</th>
              <th>Matches</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="9" style={{ textAlign: 'center', padding: '2rem' }}><div className="spinner" style={{ margin: '0 auto' }} /></td></tr>
            ) : patients.length === 0 ? (
              <tr><td colSpan="9" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-tertiary)' }}>No patients found</td></tr>
            ) : patients.map(p => (
              <tr key={p.patient_id} style={{ cursor: 'pointer' }} onClick={() => navigate(`/patients/${p.patient_id}`)}>
                <td><code style={{ color: 'var(--accent-light)', fontSize: '0.8rem' }}>{p.patient_id}</code></td>
                <td style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{p.first_name} {p.last_name}</td>
                <td><span className={`badge ${p.gender === 'F' ? 'badge-accent' : 'badge-info'}`}>{p.gender}</span></td>
                <td>{p.date_of_birth ? new Date(p.date_of_birth).toLocaleDateString() : '-'}</td>
                <td>{p.blood_type || '-'}</td>
                <td><span className={`badge ${p.status === 'active' ? 'badge-success' : 'badge-warning'}`}>{p.status}</span></td>
                <td style={{ color: 'var(--info)' }}>{p.notes_count || 0}</td>
                <td style={{ color: 'var(--accent-light)' }}>{p.matches_count || 0}</td>
                <td>
                  <div style={{ display: 'flex', gap: '0.35rem' }} onClick={e => e.stopPropagation()}>
                    <button className="btn btn-secondary btn-sm" onClick={() => navigate(`/patients/${p.patient_id}`)} data-tooltip="View"><Eye size={13} /></button>
                    <button className="btn btn-danger btn-sm" onClick={() => handleDelete(p.patient_id)} data-tooltip="Delete"><Trash2 size={13} /></button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {pages > 1 && (
        <div className="pagination">
          <button disabled={page <= 1} onClick={() => setPage(p => p - 1)}><ChevronLeft size={14} /></button>
          {Array.from({ length: Math.min(pages, 7) }, (_, i) => i + 1).map(p => (
            <button key={p} className={page === p ? 'active' : ''} onClick={() => setPage(p)}>{p}</button>
          ))}
          <button disabled={page >= pages} onClick={() => setPage(p => p + 1)}><ChevronRight size={14} /></button>
        </div>
      )}

      {/* Create Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Add New Patient</h2>
              <button className="modal-close" onClick={() => setShowModal(false)}>✕</button>
            </div>
            <form onSubmit={handleCreate}>
              <div className="modal-body">
                <div className="grid-2">
                  <div className="form-group">
                    <label>First Name</label>
                    <input className="form-input" required value={form.first_name} onChange={e => setForm({ ...form, first_name: e.target.value })} />
                  </div>
                  <div className="form-group">
                    <label>Last Name</label>
                    <input className="form-input" required value={form.last_name} onChange={e => setForm({ ...form, last_name: e.target.value })} />
                  </div>
                </div>
                <div className="grid-2">
                  <div className="form-group">
                    <label>Date of Birth</label>
                    <input className="form-input" type="date" required value={form.date_of_birth} onChange={e => setForm({ ...form, date_of_birth: e.target.value })} />
                  </div>
                  <div className="form-group">
                    <label>Gender</label>
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
                      <option value="">Select</option>
                      {['A+','A-','B+','B-','AB+','AB-','O+','O-'].map(bt => <option key={bt} value={bt}>{bt}</option>)}
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Ethnicity</label>
                    <input className="form-input" value={form.ethnicity} onChange={e => setForm({ ...form, ethnicity: e.target.value })} />
                  </div>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary"><Plus size={14} /> Create Patient</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
