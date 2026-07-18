import { useState, useEffect } from 'react'
import { api } from '../utils/api'
import { Users, FileText, Dna, Activity, TrendingUp, Zap, Clock, BarChart3 } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, AreaChart, Area } from 'recharts'

// Human-curated Slate & Copper dashboard palette
const CHART_COLORS = ['#0f766e', '#ca8a04', '#10b981', '#0369a1', '#be185d', '#64748b', '#94a3b8']

// Clean, Apple-style frosted light tooltip configuration
const tooltipStyle = {
  contentStyle: {
    background: 'rgba(255, 255, 255, 0.95)',
    border: '1px solid rgba(15, 23, 42, 0.08)',
    borderRadius: '8px',
    boxShadow: '0 6px 20px rgba(15, 23, 42, 0.05)',
    fontSize: '11px',
    color: '#0f172a',
    backdropFilter: 'blur(8px)',
    padding: '8px 12px'
  },
  itemStyle: { color: '#0f172a', padding: '2px 0' },
  labelStyle: { color: '#64748b', fontWeight: 'bold', marginBottom: '4px' }
}

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [symptoms, setSymptoms] = useState([])
  const [distribution, setDistribution] = useState(null)
  const [timeline, setTimeline] = useState([])
  const [activity, setActivity] = useState([])
  const [entities, setEntities] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboard()
  }, [])

  async function loadDashboard() {
    try {
      const [s, sym, dist, tl, act, ent] = await Promise.all([
        api.getDashboard(),
        api.getSymptomFrequency(),
        api.getDiseaseDistribution(),
        api.getTimelineDensity(),
        api.getRecentActivity(10),
        api.getEntityBreakdown(),
      ])
      setStats(s)
      setSymptoms(sym.symptoms?.slice(0, 10) || [])
      setDistribution(dist)
      setTimeline(tl.timeline || [])
      setActivity(act.activities || [])
      setEntities(ent.entities || [])
    } catch (err) {
      console.error('Dashboard load error:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading-container"><div className="spinner" /></div>
  }

  const categoryData = distribution?.by_category?.slice(0, 8) || []
  const entityData = entities.map((e, i) => ({
    name: e.entity_type === 'lab_value' ? 'Lab Values' : e.entity_type.charAt(0).toUpperCase() + e.entity_type.slice(1) + 's',
    value: e.count,
    color: ['#be185d', '#047857', '#b45309', '#0369a1'][i] || '#0f766e'
  }))

  return (
    <div className="fade-in workspace-glow-bg">
      <div className="page-header">
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)' }}>Dashboard</h1>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-tertiary)' }}>System Overview & Patient Analytics</p>
        </div>
      </div>

      {/* Bento Stat Cards */}
      <div className="bento-stat-grid">
        {/* Card 1: Active Caseload */}
        <div className="bento-stat-card" style={{ borderLeftColor: 'var(--accent)' }}>
          <div className="bento-stat-header">
            <span className="bento-stat-title">Patient Caseload</span>
            <Users size={14} style={{ color: 'var(--accent)' }} />
          </div>
          <div className="bento-stat-value-group">
            <span className="bento-stat-value">{stats?.total_patients || 0}</span>
            <span className="bento-stat-unit">cases</span>
          </div>
          <div className="bento-stat-details">
            <span>Active Clinical Cases • {stats?.total_matches || 0} verified pathologies</span>
          </div>
        </div>

        {/* Card 2: Processed Case Narratives */}
        <div className="bento-stat-card" style={{ borderLeftColor: '#0369a1' }}>
          <div className="bento-stat-header">
            <span className="bento-stat-title">Clinical NLP Extraction</span>
            <FileText size={14} style={{ color: '#0369a1' }} />
          </div>
          <div className="bento-stat-value-group">
            <span className="bento-stat-value">{stats?.total_notes || 0}</span>
            <span className="bento-stat-unit">narratives</span>
          </div>
          <div className="bento-stat-details">
            <span>BioBERT Case Notes • {stats?.recent_activity_24h || 0} events (24h)</span>
          </div>
        </div>

        {/* Card 3: Cataloged Syndromes */}
        <div className="bento-stat-card" style={{ borderLeftColor: '#be185d' }}>
          <div className="bento-stat-header">
            <span className="bento-stat-title">Orphanet Registry</span>
            <Dna size={14} style={{ color: '#be185d' }} />
          </div>
          <div className="bento-stat-value-group">
            <span className="bento-stat-value">{stats?.total_diseases || 0}</span>
            <span className="bento-stat-unit">syndromes</span>
          </div>
          <div className="bento-stat-details">
            <span>Orphanet DB Integration</span>
          </div>
        </div>

        {/* Card 4: Mean Reasoning Confidence */}
        <div className="bento-stat-card" style={{ borderLeftColor: 'var(--warning)' }}>
          <div className="bento-stat-header">
            <span className="bento-stat-title">Reasoning Confidence</span>
            <Zap size={14} style={{ color: 'var(--warning)' }} />
          </div>
          <div className="bento-stat-value-group">
            <span className="bento-stat-value">{stats?.avg_confidence || 0}%</span>
            <span className="bento-stat-unit">mean</span>
          </div>
          <div className="bento-stat-details">
            <span>Phenotype Matching</span>
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid-2" style={{ marginBottom: '1.75rem' }}>
        {/* Symptom Frequency */}
        <div className="chart-container glassmorphic-panel">
          <h3 className="chart-title"><BarChart3 size={15} style={{ display: 'inline', marginRight: '0.4rem', verticalAlign: 'text-bottom' }} />Prevalent Patient Phenotypes</h3>
          {symptoms.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={symptoms} layout="vertical" margin={{ left: 10, right: 10, top: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(15,23,42,0.03)" />
                <XAxis type="number" tick={{ fill: 'var(--text-tertiary)', fontSize: 11 }} />
                <YAxis type="category" dataKey="symptom" tick={{ fill: 'var(--text-secondary)', fontSize: 11 }} width={110} />
                <Tooltip {...tooltipStyle} />
                <Bar dataKey="count" fill="var(--accent)" radius={[0, 4, 4, 0]} barSize={12} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state">
              <p>No symptom data available yet</p>
            </div>
          )}
        </div>

        {/* Disease Categories */}
        <div className="chart-container glassmorphic-panel">
          <h3 className="chart-title"><Dna size={15} style={{ display: 'inline', marginRight: '0.4rem', verticalAlign: 'text-bottom' }} />Disease Category Distribution</h3>
          {categoryData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryData}
                  dataKey="count"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  outerRadius={95}
                  innerRadius={65}
                  paddingAngle={4}
                  label={({ category, count }) => `${category} (${count})`}
                >
                  {categoryData.map((entry, i) => (
                    <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip {...tooltipStyle} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state">
              <p>No disease data available yet</p>
            </div>
          )}
        </div>
      </div>

      {/* Second Row */}
      <div className="grid-2" style={{ marginBottom: '1.75rem' }}>
        {/* Timeline Density */}
        <div className="chart-container glassmorphic-panel">
          <h3 className="chart-title"><Clock size={15} style={{ display: 'inline', marginRight: '0.4rem', verticalAlign: 'text-bottom' }} />Admissions & Consultation Trends</h3>
          {timeline.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={timeline} margin={{ top: 10, right: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(15,23,42,0.03)" />
                <XAxis dataKey="month" tick={{ fill: 'var(--text-tertiary)', fontSize: 11 }} />
                <YAxis tick={{ fill: 'var(--text-tertiary)', fontSize: 11 }} />
                <Tooltip {...tooltipStyle} />
                <defs>
                  <linearGradient id="colorVisits" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--accent)" stopOpacity={0.25} />
                    <stop offset="100%" stopColor="var(--accent)" stopOpacity={0.02} />
                  </linearGradient>
                </defs>
                <Area type="monotone" dataKey="visit_count" stroke="var(--accent)" fill="url(#colorVisits)" strokeWidth={1.5} name="Visits" />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state">
              <p>No timeline data available yet</p>
            </div>
          )}
        </div>

        {/* Entity Breakdown */}
        <div className="chart-container glassmorphic-panel">
          <h3 className="chart-title"><Zap size={15} style={{ display: 'inline', marginRight: '0.4rem', verticalAlign: 'text-bottom' }} />Extracted Clinical Entities (Phenopackets)</h3>
          {entityData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={entityData} margin={{ top: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(15,23,42,0.03)" />
                <XAxis dataKey="name" tick={{ fill: 'var(--text-tertiary)', fontSize: 11 }} />
                <YAxis tick={{ fill: 'var(--text-tertiary)', fontSize: 11 }} />
                <Tooltip {...tooltipStyle} />
                <Bar dataKey="value" radius={[4, 4, 0, 0]} barSize={24}>
                  {entityData.map((entry, i) => (
                    <Cell key={i} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state">
              <p>No entity data available yet</p>
            </div>
          )}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="chart-container glassmorphic-panel">
        <h3 className="chart-title"><Activity size={15} style={{ display: 'inline', marginRight: '0.4rem', verticalAlign: 'text-bottom' }} />Workstation Audit Logs</h3>
        {activity.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {activity.map((a, i) => (
              <div key={i} className="recent-activity-row" style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                padding: '0.65rem 0.85rem',
                background: 'rgba(15, 23, 42, 0.015)',
                border: '1px solid rgba(15, 23, 42, 0.03)',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.82rem'
              }}>
                <span className={`badge badge-${
                  a.action.includes('match') ? 'accent' : 
                  a.action.includes('note') ? 'info' : 
                  a.action.includes('patient') ? 'success' : 
                  a.action.includes('search') ? 'warning' : 'accent'
                }`}>
                  {a.action.replace(/_/g, ' ')}
                </span>
                <span style={{ color: 'var(--text-secondary)', flex: 1 }}>{a.details}</span>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.72rem', whiteSpace: 'nowrap', fontFamily: 'monospace' }}>
                  {a.timestamp ? new Date(a.timestamp).toLocaleString() : ''}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state" style={{ padding: '2rem' }}>
            <p>No activity logged yet</p>
          </div>
        )}
      </div>
    </div>
  )
}
