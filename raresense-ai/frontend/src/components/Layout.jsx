import { NavLink, useLocation } from 'react-router-dom'
import { LayoutDashboard, Users, Dna, Search, BrainCircuit, LogOut, Activity, Database } from 'lucide-react'

const clinicianNavItems = [
  { section: 'Overview' },
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { section: 'Clinical' },
  { path: '/patients', label: 'Patients', icon: Users },
  { path: '/diseases', label: 'Disease Database', icon: Dna },
  { section: 'Intelligence' },
  { path: '/search', label: 'Search & Filter', icon: Search },
  { path: '/ai-assistant', label: 'AI Assistant', icon: BrainCircuit },
]

const patientNavItems = [
  { section: 'My Health' },
  { path: '/patient-dashboard', label: 'My Timeline', icon: Activity },
]

export default function Layout({ children, user, onLogout }) {
  const location = useLocation()
  const navItems = user?.role === 'patient' ? patientNavItems : clinicianNavItems

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <div className="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" style={{ width: '22px', height: '22px', color: 'var(--accent)' }}>
              <path d="M4.5 16.5c3-4.5 3-4.5 6-9s3-4.5 6-9" />
              <path d="M4.5 7.5c3 4.5 3 4.5 6 9s3 4.5 6 9" opacity="0.3" />
              <circle cx="12" cy="12" r="9" strokeWidth="1.5" strokeDasharray="3 2" />
              <circle cx="10.5" cy="7.5" r="1.5" fill="var(--accent)" stroke="none" />
              <circle cx="13.5" cy="16.5" r="1.5" fill="var(--accent)" stroke="none" />
            </svg>
          </div>
          <div className="logo-text">
            <h1>RareSense.AI</h1>
            <span>Rare Disease Detection</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item, idx) =>
            item.section ? (
              <div key={idx} className="nav-section-title">{item.section}</div>
            ) : (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `nav-link${isActive && (item.path === '/' ? location.pathname === '/' : true) ? ' active' : ''}`
                }
                end={item.path === '/'}
              >
                <item.icon />
                {item.label}
              </NavLink>
            )
          )}
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">
              {user?.full_name?.split(' ').map(n => n[0]).join('').slice(0, 2) || 'U'}
            </div>
            <div className="user-details">
              <div className="name">{user?.full_name || 'User'}</div>
              <div className="role">{user?.role || 'clinician'}</div>
            </div>
          </div>
          <button
            className="btn btn-secondary btn-sm"
            onClick={onLogout}
            style={{ marginTop: '0.75rem', width: '100%', justifyContent: 'center' }}
          >
            <LogOut size={14} />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content fade-in">
        {children}
      </main>
    </div>
  )
}
