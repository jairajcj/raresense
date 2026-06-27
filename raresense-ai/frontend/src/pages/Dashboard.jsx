import { useState, useEffect } from 'react'
import { api } from '../utils/api'
import { Users, FileText, Dna, Activity, TrendingUp, Zap, Clock, BarChart3 } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, AreaChart, Area } from 'recharts'

const CHART_COLORS = ['#6366f1', '#a855f7', '#ec4899', '#f43f5e', '#f97316', '#eab308', '#22c55e', '#06b6d4', '#3b82f6', '#8b5cf6']

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
    color: ['#f472b6', '#34d399', '#fbbf24', '#60a5fa'][i] || '#6366f1'
  }))

  return (
    <div className="fade-in">
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p>RareSense.AI system overview and analytics</p>
        </div>
      </div>

      {/* Stat Cards */}
      <div className="stat-grid">
        <div className="stat-card" style={{ '--stat-color': '#6366f1' }}>
          <div className="stat-icon" style={{ background: 'rgba(99,102,241,0.15)', color: '#818cf8' }}>
            <Users />
          </div>
          <div className="stat-info">
            <h3>{stats?.total_patients || 0}</h3>
            <p>Total Patients</p>
          </div>
        </div>

        <div className="stat-card" style={{ '--stat-color': '#a855f7' }}>
          <div className="stat-icon" style={{ background: 'rgba(168,85,247,0.15)', color: '#c084fc' }}>
            <FileText />
          </div>
          <div className="stat-info">
            <h3>{stats?.total_notes || 0}</h3>
            <p>Clinical Notes</p>
          </div>
        </div>

        <div className="stat-card" style={{ '--stat-color': '#ec4899' }}>
          <div className="stat-icon" style={{ background: 'rgba(236,72,153,0.15)', color: '#f472b6' }}>
            <Dna />
          </div>
          <div className="stat-info">
            <h3>{stats?.total_diseases || 0}</h3>
            <p>Rare Diseases</p>
          </div>
        </div>

        <div className="stat-card" style={{ '--stat-color': '#10b981' }}>
          <div className="stat-icon" style={{ background: 'rgba(16,185,129,0.15)', color: '#34d399' }}>
            <TrendingUp />
          </div>
          <div className="stat-info">
            <h3>{stats?.total_matches || 0}</h3>
            <p>Disease Matches</p>
          </div>
        </div>

        <div className="stat-card" style={{ '--stat-color': '#f59e0b' }}>
          <div className="stat-icon" style={{ background: 'rgba(245,158,11,0.15)', color: '#fbbf24' }}>
            <Zap />
          </div>
          <div className="stat-info">
            <h3>{stats?.avg_confidence || 0}%</h3>
            <p>Avg Match Confidence</p>
          </div>
        </div>

        <div className="stat-card" style={{ '--stat-color': '#06b6d4' }}>
          <div className="stat-icon" style={{ background: 'rgba(6,182,212,0.15)', color: '#22d3ee' }}>
            <Activity />
          </div>
          <div className="stat-info">
            <h3>{stats?.recent_activity_24h || 0}</h3>
            <p>Activity (24h)</p>
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid-2" style={{ marginBottom: '1.5rem' }}>
        {/* Symptom Frequency */}
        <div className="chart-container">
          <h3><BarChart3 size={16} style={{ display: 'inline', marginRight: '0.5rem', verticalAlign: 'text-bottom' }} />Top Extracted Symptoms</h3>
          {symptoms.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={symptoms} layout="vertical" margin={{ left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
                <XAxis type="number" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <YAxis type="category" dataKey="symptom" tick={{ fill: '#94a3b8', fontSize: 11 }} width={120} />
                <Tooltip
                  contentStyle={{ background: '#1a1f35', border: '1px solid rgba(148,163,184,0.2)', borderRadius: 8, fontSize: 12 }}
                  itemStyle={{ color: '#f1f5f9' }}
                />
                <Bar dataKey="count" fill="#6366f1" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state" style={{ padding: '2rem' }}>
              <p>No symptom data available yet</p>
            </div>
          )}
        </div>

        {/* Disease Categories */}
        <div className="chart-container">
          <h3><Dna size={16} style={{ display: 'inline', marginRight: '0.5rem', verticalAlign: 'text-bottom' }} />Disease Categories</h3>
          {categoryData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryData}
                  dataKey="count"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  innerRadius={55}
                  paddingAngle={3}
                  label={({ category, count }) => `${category} (${count})`}
                >
                  {categoryData.map((entry, i) => (
                    <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ background: '#1a1f35', border: '1px solid rgba(148,163,184,0.2)', borderRadius: 8, fontSize: 12 }}
                  itemStyle={{ color: '#f1f5f9' }}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state" style={{ padding: '2rem' }}>
              <p>No disease data available yet</p>
            </div>
          )}
        </div>
      </div>

      {/* Second Row */}
      <div className="grid-2" style={{ marginBottom: '1.5rem' }}>
        {/* Timeline Density */}
        <div className="chart-container">
          <h3><Clock size={16} style={{ display: 'inline', marginRight: '0.5rem', verticalAlign: 'text-bottom' }} />Clinical Visits Over Time</h3>
          {timeline.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={timeline}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
                <XAxis dataKey="month" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ background: '#1a1f35', border: '1px solid rgba(148,163,184,0.2)', borderRadius: 8, fontSize: 12 }}
                  itemStyle={{ color: '#f1f5f9' }}
                />
                <defs>
                  <linearGradient id="colorVisits" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#6366f1" stopOpacity={0.3} />
                    <stop offset="100%" stopColor="#6366f1" stopOpacity={0.05} />
                  </linearGradient>
                </defs>
                <Area type="monotone" dataKey="visit_count" stroke="#6366f1" fill="url(#colorVisits)" strokeWidth={2} name="Visits" />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state" style={{ padding: '2rem' }}>
              <p>No timeline data available yet</p>
            </div>
          )}
        </div>

        {/* Entity Breakdown */}
        <div className="chart-container">
          <h3><Zap size={16} style={{ display: 'inline', marginRight: '0.5rem', verticalAlign: 'text-bottom' }} />NLP Entity Breakdown</h3>
          {entityData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={entityData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
                <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ background: '#1a1f35', border: '1px solid rgba(148,163,184,0.2)', borderRadius: 8, fontSize: 12 }}
                  itemStyle={{ color: '#f1f5f9' }}
                />
                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                  {entityData.map((entry, i) => (
                    <Cell key={i} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state" style={{ padding: '2rem' }}>
              <p>No entity data available yet</p>
            </div>
          )}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="chart-container">
        <h3><Activity size={16} style={{ display: 'inline', marginRight: '0.5rem', verticalAlign: 'text-bottom' }} />Recent Activity</h3>
        {activity.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {activity.map((a, i) => (
              <div key={i} style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                padding: '0.6rem 0.85rem',
                background: 'var(--bg-elevated)',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.8rem'
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
                <span style={{ color: 'var(--text-muted)', fontSize: '0.7rem', whiteSpace: 'nowrap' }}>
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
