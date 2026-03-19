import { useEffect, useState } from 'react'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const features = [
  { icon: '👥', title: 'Employee Management', desc: 'Add, edit & manage employee profiles with department assignment' },
  { icon: '📅', title: 'Attendance Tracking', desc: 'Mark daily attendance — Present, Absent, Late, or Half Day' },
  { icon: '📊', title: 'Live Dashboard', desc: 'Real-time stats: attendance rate, department breakdown & summaries' },
  { icon: '🔔', title: 'Toast Notifications', desc: 'Instant feedback on every action with clean toast alerts' },
]

const techStack = ['FastAPI', 'PostgreSQL', 'React', 'Vite', 'Render', 'Vercel']

export default function WakeUpScreen({ onReady }) {
  const [elapsed, setElapsed] = useState(0)
  const [status, setStatus] = useState('waking') // 'waking' | 'ready' | 'error'
  const [dots, setDots] = useState('')

  useEffect(() => {
    // Animate ellipsis
    const dotsInterval = setInterval(() => {
      setDots(d => d.length >= 3 ? '' : d + '.')
    }, 500)

    // Elapsed timer
    const timer = setInterval(() => setElapsed(e => e + 1), 1000)

    // Wake up the backend by polling /api/dashboard/stats
    const MAX_RETRIES = 20
    let attempts = 0
    let stopped = false

    async function ping() {
      if (stopped) return
      try {
        const res = await fetch(`${BASE_URL}/api/dashboard/stats`, { signal: AbortSignal.timeout(8000) })
        if (res.ok) {
          stopped = true
          clearInterval(dotsInterval)
          clearInterval(timer)
          setStatus('ready')
          setTimeout(() => onReady(), 600)
          return
        }
      } catch (_) {}
      attempts++
      if (attempts >= MAX_RETRIES) {
        stopped = true
        clearInterval(dotsInterval)
        clearInterval(timer)
        setStatus('error')
        return
      }
      setTimeout(ping, 3000)
    }

    ping()

    return () => {
      stopped = true
      clearInterval(dotsInterval)
      clearInterval(timer)
    }
  }, [])

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: "'Inter', 'Segoe UI', sans-serif",
      padding: '24px',
    }}>
      <div style={{ maxWidth: 680, width: '100%' }}>

        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: 40 }}>
          <div style={{ fontSize: 48, marginBottom: 8 }}>⚡</div>
          <h1 style={{ color: '#f1f5f9', fontSize: 32, fontWeight: 700, margin: '0 0 8px' }}>
            HRMS Lite
          </h1>
          <p style={{ color: '#94a3b8', fontSize: 16, margin: 0 }}>
            Human Resource Management System
          </p>
        </div>

        {/* Wake-up status card */}
        <div style={{
          background: 'rgba(30,41,59,0.8)',
          border: '1px solid rgba(99,102,241,0.3)',
          borderRadius: 16,
          padding: '28px 32px',
          marginBottom: 28,
          backdropFilter: 'blur(8px)',
        }}>
          {status === 'waking' && (
            <>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
                <div style={{
                  width: 12, height: 12, borderRadius: '50%',
                  background: '#f59e0b',
                  boxShadow: '0 0 8px #f59e0b',
                  animation: 'pulse 1.2s infinite',
                }} />
                <span style={{ color: '#fbbf24', fontWeight: 600, fontSize: 15 }}>
                  Waking up the server{dots}
                </span>
                <span style={{ marginLeft: 'auto', color: '#64748b', fontSize: 13 }}>
                  {elapsed}s
                </span>
              </div>
              <div style={{ background: '#0f172a', borderRadius: 8, padding: '10px 14px', marginBottom: 16 }}>
                <p style={{ color: '#64748b', fontSize: 13, margin: 0, lineHeight: 1.6 }}>
                  🆓 <strong style={{ color: '#94a3b8' }}>Free tier notice:</strong> The backend is hosted on
                  Render's free plan. After periods of inactivity, it needs{' '}
                  <strong style={{ color: '#fbbf24' }}>40–60 seconds</strong> to spin up.
                  Hang tight — it's booting!
                </p>
              </div>
              {/* Progress bar */}
              <div style={{ background: '#1e293b', borderRadius: 999, height: 6, overflow: 'hidden' }}>
                <div style={{
                  height: '100%',
                  borderRadius: 999,
                  background: 'linear-gradient(90deg, #6366f1, #8b5cf6)',
                  width: `${Math.min((elapsed / 60) * 100, 95)}%`,
                  transition: 'width 1s linear',
                }} />
              </div>
            </>
          )}
          {status === 'ready' && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#22c55e', boxShadow: '0 0 8px #22c55e' }} />
              <span style={{ color: '#4ade80', fontWeight: 600, fontSize: 15 }}>Server is live! Loading app{dots}</span>
            </div>
          )}
          {status === 'error' && (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12 }}>
                <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#ef4444' }} />
                <span style={{ color: '#f87171', fontWeight: 600, fontSize: 15 }}>Server took too long to respond</span>
              </div>
              <button
                onClick={() => window.location.reload()}
                style={{
                  background: '#6366f1', color: '#fff', border: 'none', borderRadius: 8,
                  padding: '8px 20px', cursor: 'pointer', fontWeight: 600, fontSize: 14,
                }}
              >
                Retry
              </button>
            </div>
          )}
        </div>

        {/* Features grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14, marginBottom: 24 }}>
          {features.map(f => (
            <div key={f.title} style={{
              background: 'rgba(30,41,59,0.6)',
              border: '1px solid rgba(255,255,255,0.06)',
              borderRadius: 12,
              padding: '16px 18px',
            }}>
              <div style={{ fontSize: 22, marginBottom: 6 }}>{f.icon}</div>
              <div style={{ color: '#e2e8f0', fontWeight: 600, fontSize: 14, marginBottom: 4 }}>{f.title}</div>
              <div style={{ color: '#64748b', fontSize: 12, lineHeight: 1.5 }}>{f.desc}</div>
            </div>
          ))}
        </div>

        {/* Tech stack */}
        <div style={{ textAlign: 'center' }}>
          <p style={{ color: '#475569', fontSize: 12, marginBottom: 10 }}>BUILT WITH</p>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', justifyContent: 'center' }}>
            {techStack.map(t => (
              <span key={t} style={{
                background: 'rgba(99,102,241,0.15)',
                border: '1px solid rgba(99,102,241,0.3)',
                color: '#a5b4fc',
                borderRadius: 999,
                padding: '4px 14px',
                fontSize: 12,
                fontWeight: 500,
              }}>{t}</span>
            ))}
          </div>
          <p style={{ color: '#334155', fontSize: 11, marginTop: 20 }}>
            github.com/kapilraghav2801/HRMS
          </p>
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      `}</style>
    </div>
  )
}
