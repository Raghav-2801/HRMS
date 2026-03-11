import { NavLink, useLocation } from 'react-router-dom'

const routes = [
  {
    path: '/', label: 'Dashboard',
    icon: <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M3 7h7v7H3zM14 3h7v4h-7zM14 12h7v9h-7zM3 17h7v4H3z" /></svg>
  },
  {
    path: '/employees', label: 'Employees',
    icon: <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
  },
  {
    path: '/attendance', label: 'Attendance',
    icon: <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" /></svg>
  }
]

const pageTitles = {
  '/': 'Dashboard',
  '/employees': 'Employee Management',
  '/attendance': 'Attendance Tracking',
}

export default function Layout({ children }) {
  const location = useLocation()
  const title = pageTitles[location.pathname] || 'HRMS'

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-logo">
          <h1>⚡ HRMS Lite</h1>
          <span>Human Resource Portal</span>
        </div>
        <nav className="sidebar-nav">
          <div className="nav-label">Menu</div>
          {routes.map(r => (
            <NavLink
              key={r.path}
              to={r.path}
              end={r.path === '/'}
              className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
            >
              {r.icon}
              {r.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <div className="main-content">
        <header className="topbar">
          <span className="topbar-title">{title}</span>
          <div className="topbar-right">
            <span className="topbar-badge">Admin</span>
          </div>
        </header>
        <main className="page-body">{children}</main>
      </div>
    </div>
  )
}
