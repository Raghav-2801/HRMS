import { useEffect, useState } from 'react'
import { getDashboardStats } from '../api'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getDashboardStats()
      .then(r => setStats(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="spinner" />

  if (!stats) return (
    <div className="empty-state">
      <p>Could not load dashboard. Make sure the backend is running.</p>
    </div>
  )

  const maxDept = Math.max(...(stats.department_breakdown?.map(d => d.count) || [1]))

  return (
    <div>
      {/* Stat Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#eff6ff' }}>
            <svg fill="none" viewBox="0 0 24 24" stroke="#1d4ed8" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <div>
            <div className="stat-label">Total Employees</div>
            <div className="stat-value">{stats.total_employees}</div>
            <div className="stat-sub">{stats.total_departments} departments</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#ecfdf5' }}>
            <svg fill="none" viewBox="0 0 24 24" stroke="#059669" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <div className="stat-label">Today Present</div>
            <div className="stat-value" style={{ color: '#059669' }}>{stats.today.present}</div>
            <div className="stat-sub">{stats.today.late} late · {stats.today.half_day} half-day</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#fef2f2' }}>
            <svg fill="none" viewBox="0 0 24 24" stroke="#dc2626" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <div className="stat-label">Today Absent</div>
            <div className="stat-value" style={{ color: '#dc2626' }}>{stats.today.absent}</div>
            <div className="stat-sub">{stats.today.unmarked} not marked yet</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#fffbeb' }}>
            <svg fill="none" viewBox="0 0 24 24" stroke="#d97706" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <div>
            <div className="stat-label">Attendance Rate</div>
            <div className="stat-value" style={{ color: '#d97706' }}>{stats.attendance_rate}%</div>
            <div className="stat-sub">all-time average</div>
          </div>
        </div>
      </div>

      {/* Attendance Rate Bar */}
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-body">
          <div style={{ fontWeight: 600, marginBottom: 4 }}>Overall Attendance Rate</div>
          <div className="progress-wrap">
            <div className="progress-label">
              <span>0%</span><span>{stats.attendance_rate}%</span>
            </div>
            <div className="progress-track">
              <div className="progress-fill" style={{ width: `${stats.attendance_rate}%` }} />
            </div>
          </div>
        </div>
      </div>

      <div className="grid-2">
        {/* Today's Summary */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">Today's Summary</span>
            <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>{new Date().toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'short' })}</span>
          </div>
          <div className="card-body">
            <div className="today-grid">
              <div className="today-item">
                <div className="val" style={{ color: 'var(--green)' }}>{stats.today.present}</div>
                <div className="lbl">Present</div>
              </div>
              <div className="today-item">
                <div className="val" style={{ color: 'var(--red)' }}>{stats.today.absent}</div>
                <div className="lbl">Absent</div>
              </div>
              <div className="today-item">
                <div className="val" style={{ color: 'var(--amber)' }}>{stats.today.late}</div>
                <div className="lbl">Late</div>
              </div>
              <div className="today-item">
                <div className="val" style={{ color: 'var(--purple)' }}>{stats.today.half_day}</div>
                <div className="lbl">Half Day</div>
              </div>
            </div>
          </div>
        </div>

        {/* Department Breakdown */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">Department Breakdown</span>
          </div>
          <div className="card-body">
            {stats.department_breakdown?.length === 0
              ? <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>No departments yet.</p>
              : stats.department_breakdown.map(d => (
                <div key={d.department} className="dept-bar">
                  <div className="dept-bar-label">
                    <span>{d.department}</span>
                    <span style={{ color: 'var(--text-muted)' }}>{d.count}</span>
                  </div>
                  <div className="dept-bar-track">
                    <div className="dept-bar-fill" style={{ width: `${(d.count / maxDept) * 100}%` }} />
                  </div>
                </div>
              ))
            }
          </div>
        </div>

        {/* Recent Employees */}
        <div className="card" style={{ gridColumn: '1 / -1' }}>
          <div className="card-header">
            <span className="card-title">Recently Added Employees</span>
          </div>
          <div className="card-body">
            {stats.recent_employees?.length === 0
              ? <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>No employees yet.</p>
              : <div className="recent-list">
                  {stats.recent_employees.map(e => (
                    <div key={e.id} className="recent-item">
                      <div className="avatar">{e.name.charAt(0).toUpperCase()}</div>
                      <div className="recent-item-info">
                        <div className="name">{e.name}</div>
                        <div className="dept">{e.employee_id} · {e.department}</div>
                      </div>
                    </div>
                  ))}
                </div>
            }
          </div>
        </div>
      </div>
    </div>
  )
}
