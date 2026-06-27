import { useState, useEffect } from 'react'
import { api } from '../utils/api'
import { Search, Dna, ChevronLeft, ChevronRight } from 'lucide-react'

export default function Diseases() {
  const [diseases, setDiseases] = useState([])
  const [categories, setCategories] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [selectedDisease, setSelectedDisease] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => { loadDiseases(); loadCategories() }, [page, category])

  async function loadDiseases() {
    setLoading(true)
    try {
      let params = `?page=${page}&limit=15`
      if (search) params += `&search=${search}`
      if (category) params += `&category=${category}`
      const data = await api.getDiseases(params)
      setDiseases(data.diseases || [])
      setTotal(data.total || 0)
      setPages(data.pages || 1)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  async function loadCategories() {
    try {
      const data = await api.getCategories()
      setCategories(data.categories || [])
    } catch (err) {
      console.error(err)
    }
  }

  function handleSearch(e) {
    e.preventDefault()
    setPage(1)
    loadDiseases()
  }

  const freqColor = { very_frequent: 'badge-danger', frequent: 'badge-warning', occasional: 'badge-info', rare: 'badge-accent' }

  return (
    <div className="fade-in">
      <div className="page-header">
        <div>
          <h1>Disease Database</h1>
          <p>{total} rare diseases from Orphanet/HPO</p>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <form onSubmit={handleSearch} className="search-bar">
            <Search />
            <input placeholder="Search diseases..." value={search} onChange={e => setSearch(e.target.value)} />
          </form>
          <select className="form-select" style={{ width: '180px' }} value={category} onChange={e => { setCategory(e.target.value); setPage(1) }}>
            <option value="">All Categories</option>
            {categories.map(c => <option key={c.category} value={c.category}>{c.category} ({c.count})</option>)}
          </select>
        </div>
      </div>

      {/* Disease Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '1rem' }}>
        {loading ? (
          <div className="loading-container" style={{ gridColumn: '1/-1' }}><div className="spinner" /></div>
        ) : diseases.length === 0 ? (
          <div className="empty-state" style={{ gridColumn: '1/-1' }}>
            <Dna size={48} />
            <h3>No diseases found</h3>
            <p>Try a different search query</p>
          </div>
        ) : diseases.map(d => (
          <div key={d._id} className="card" style={{ cursor: 'pointer' }} onClick={() => setSelectedDisease(d)}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
              <div>
                <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.3 }}>{d.name}</h3>
                <code style={{ fontSize: '0.7rem', color: 'var(--accent-light)' }}>{d.orpha_id}</code>
              </div>
              <span className="badge badge-accent">{d.category}</span>
            </div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', marginBottom: '0.75rem', lineHeight: 1.5, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
              {d.description}
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', fontSize: '0.7rem', color: 'var(--text-muted)' }}>
              <span>🧬 {d.symptoms?.length || 0} symptoms</span>
              <span>📊 {d.prevalence}</span>
              <span>🧪 {d.inheritance}</span>
            </div>
          </div>
        ))}
      </div>

      {pages > 1 && (
        <div className="pagination">
          <button disabled={page <= 1} onClick={() => setPage(p => p - 1)}><ChevronLeft size={14} /></button>
          {Array.from({ length: Math.min(pages, 7) }, (_, i) => i + 1).map(p => (
            <button key={p} className={page === p ? 'active' : ''} onClick={() => setPage(p)}>{p}</button>
          ))}
          <button disabled={page >= pages} onClick={() => setPage(p => p + 1)}><ChevronRight size={14} /></button>
        </div>
      )}

      {/* Disease Detail Modal */}
      {selectedDisease && (
        <div className="modal-overlay" onClick={() => setSelectedDisease(null)}>
          <div className="modal" onClick={e => e.stopPropagation()} style={{ maxWidth: '700px' }}>
            <div className="modal-header">
              <div>
                <h2>{selectedDisease.name}</h2>
                <code style={{ fontSize: '0.75rem', color: 'var(--accent-light)' }}>{selectedDisease.orpha_id}</code>
              </div>
              <button className="modal-close" onClick={() => setSelectedDisease(null)}>✕</button>
            </div>
            <div className="modal-body">
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1.25rem', lineHeight: 1.6 }}>
                {selectedDisease.description}
              </p>

              <div className="grid-3" style={{ marginBottom: '1.25rem', gap: '0.75rem' }}>
                <div style={{ padding: '0.75rem', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-sm)' }}>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Category</div>
                  <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>{selectedDisease.category}</div>
                </div>
                <div style={{ padding: '0.75rem', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-sm)' }}>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Prevalence</div>
                  <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>{selectedDisease.prevalence}</div>
                </div>
                <div style={{ padding: '0.75rem', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-sm)' }}>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Inheritance</div>
                  <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>{selectedDisease.inheritance}</div>
                </div>
              </div>

              <h4 style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.75rem', color: 'var(--text-primary)' }}>
                Associated Symptoms ({selectedDisease.symptoms?.length || 0})
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                {selectedDisease.symptoms?.map((s, i) => (
                  <div key={i} style={{
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    padding: '0.5rem 0.75rem', background: 'var(--bg-input)', borderRadius: 'var(--radius-sm)'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span className="entity-tag symptom" style={{ margin: 0 }}>{s.name}</span>
                      <code style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>{s.hpo_code}</code>
                    </div>
                    <span className={`badge ${freqColor[s.frequency] || 'badge-accent'}`}>{s.frequency?.replace(/_/g, ' ')}</span>
                  </div>
                ))}
              </div>

              {selectedDisease.gene_associations?.length > 0 && (
                <div style={{ marginTop: '1.25rem' }}>
                  <h4 style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.5rem' }}>Gene Associations</h4>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem' }}>
                    {selectedDisease.gene_associations.map((g, i) => (
                      <span key={i} className="badge badge-info">{g}</span>
                    ))}
                  </div>
                </div>
              )}

              {selectedDisease.synonyms?.length > 0 && (
                <div style={{ marginTop: '1rem' }}>
                  <h4 style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.5rem' }}>Synonyms</h4>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)' }}>{selectedDisease.synonyms.join(', ')}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
