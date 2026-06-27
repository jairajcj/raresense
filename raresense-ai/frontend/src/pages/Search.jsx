import { useState } from 'react'
import { api } from '../utils/api'
import { useNavigate } from 'react-router-dom'
import { Search as SearchIcon, Filter, FileText, Calendar, Stethoscope, X } from 'lucide-react'

export default function Search() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)
  const [tab, setTab] = useState('text')
  const [filters, setFilters] = useState({ specialty: '', note_type: '', date_from: '', date_to: '', symptom: '' })
  const navigate = useNavigate()

  async function handleSearch(e) {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    setSearched(true)
    try {
      const data = await api.search(query)
      setResults(data.results || [])
      setTotal(data.total || 0)
    } catch (err) {
      console.error(err)
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  async function handleFilter(e) {
    e.preventDefault()
    setLoading(true)
    setSearched(true)
    try {
      const params = new URLSearchParams()
      Object.entries(filters).forEach(([k, v]) => { if (v) params.set(k, v) })
      const data = await api.filterNotes(params.toString())
      setResults(data.results || [])
      setTotal(data.total || 0)
    } catch (err) {
      console.error(err)
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  const entityTypeColor = { symptom: 'symptom', medication: 'medication', diagnosis: 'diagnosis', lab_value: 'lab_value' }

  return (
    <div className="fade-in">
      <div className="page-header">
        <div>
          <h1>Search & Filter</h1>
          <p>Full-text search across clinical notes using MongoDB text indexes</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button className={`tab ${tab === 'text' ? 'active' : ''}`} onClick={() => setTab('text')}>
          <SearchIcon size={14} style={{ display: 'inline', marginRight: '0.35rem', verticalAlign: 'text-bottom' }} />
          Text Search
        </button>
        <button className={`tab ${tab === 'filter' ? 'active' : ''}`} onClick={() => setTab('filter')}>
          <Filter size={14} style={{ display: 'inline', marginRight: '0.35rem', verticalAlign: 'text-bottom' }} />
          Advanced Filter
        </button>
      </div>

      {/* Text Search */}
      {tab === 'text' && (
        <form onSubmit={handleSearch} style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <div className="search-bar" style={{ flex: 1, maxWidth: 'none' }}>
              <SearchIcon />
              <input
                placeholder="Search clinical notes... (e.g., malar rash, thrombocytopenia, lupus)"
                value={query}
                onChange={e => setQuery(e.target.value)}
                style={{ paddingRight: query ? '2.5rem' : undefined }}
              />
              {query && (
                <button type="button" onClick={() => setQuery('')} style={{
                  position: 'absolute', right: '0.5rem', top: '50%', transform: 'translateY(-50%)',
                  background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer'
                }}><X size={14} /></button>
              )}
            </div>
            <button className="btn btn-primary" type="submit" disabled={loading}>
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
          <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.75rem', flexWrap: 'wrap' }}>
            {['malar rash', 'thrombocytopenia', 'proteinuria', 'fatigue', 'lupus', 'arthralgia'].map(term => (
              <button key={term} type="button" className="btn btn-secondary btn-sm" onClick={() => { setQuery(term); }}>
                {term}
              </button>
            ))}
          </div>
        </form>
      )}

      {/* Advanced Filter */}
      {tab === 'filter' && (
        <form onSubmit={handleFilter} className="card" style={{ marginBottom: '1.5rem' }}>
          <div className="grid-3" style={{ gap: '0.75rem' }}>
            <div className="form-group">
              <label>Specialty</label>
              <select className="form-select" value={filters.specialty} onChange={e => setFilters({ ...filters, specialty: e.target.value })}>
                <option value="">All</option>
                {['Dermatology', 'Hematology', 'Nephrology', 'Primary Care', 'Rheumatology', 'Neurology', 'Cardiology', 'Pulmonology'].map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Note Type</label>
              <select className="form-select" value={filters.note_type} onChange={e => setFilters({ ...filters, note_type: e.target.value })}>
                <option value="">All</option>
                <option value="consultation">Consultation</option>
                <option value="discharge_summary">Discharge Summary</option>
                <option value="progress_note">Progress Note</option>
              </select>
            </div>
            <div className="form-group">
              <label>Symptom</label>
              <input className="form-input" placeholder="e.g., Fatigue" value={filters.symptom} onChange={e => setFilters({ ...filters, symptom: e.target.value })} />
            </div>
            <div className="form-group">
              <label>Date From</label>
              <input className="form-input" type="date" value={filters.date_from} onChange={e => setFilters({ ...filters, date_from: e.target.value })} />
            </div>
            <div className="form-group">
              <label>Date To</label>
              <input className="form-input" type="date" value={filters.date_to} onChange={e => setFilters({ ...filters, date_to: e.target.value })} />
            </div>
            <div className="form-group" style={{ display: 'flex', alignItems: 'flex-end' }}>
              <button className="btn btn-primary" type="submit" disabled={loading} style={{ width: '100%' }}>
                <Filter size={14} /> {loading ? 'Filtering...' : 'Apply Filters'}
              </button>
            </div>
          </div>
        </form>
      )}

      {/* Results */}
      {searched && (
        <div>
          <h3 style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            {total} result{total !== 1 ? 's' : ''} found
          </h3>

          {loading ? (
            <div className="loading-container"><div className="spinner" /></div>
          ) : results.length === 0 ? (
            <div className="empty-state">
              <SearchIcon size={48} />
              <h3>No results found</h3>
              <p>Try different search terms or filters</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {results.map((r, i) => (
                <div key={i} className="card" style={{ cursor: 'pointer' }} onClick={() => navigate(`/patients/${r.patient_id}`)}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                    <div>
                      <span style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{r.patient_name || r.patient_id}</span>
                      <span style={{ marginLeft: '0.5rem' }} className="badge badge-info">{r.specialty}</span>
                      <span style={{ marginLeft: '0.35rem' }} className="badge badge-accent">{r.note_type?.replace(/_/g, ' ')}</span>
                    </div>
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                      {r.date ? new Date(r.date).toLocaleDateString() : ''}
                    </span>
                  </div>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '0.5rem' }}>
                    {r.text?.substring(0, 250)}...
                  </p>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.2rem' }}>
                    {r.extracted_entities?.slice(0, 8).map((e, j) => (
                      <span key={j} className={`entity-tag ${entityTypeColor[e.entity_type] || 'symptom'}`}>
                        {e.normalized_name}
                      </span>
                    ))}
                    {(r.extracted_entities?.length || 0) > 8 && (
                      <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', padding: '0.25rem 0.5rem' }}>
                        +{r.extracted_entities.length - 8} more
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
