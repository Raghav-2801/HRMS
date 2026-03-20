import { useEffect, useState } from 'react'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function WakeUpScreen({ onReady }) {
  const [status, setStatus] = useState('loading')
  const [time, setTime] = useState(0)

  useEffect(() => {
    let stopped = false
    let retryTimer

    const timer = setInterval(() => {
      setTime(t => t + 1)
    }, 1000)

    const checkServer = async () => {
      if (stopped) return

      try {
        const res = await fetch(`${BASE_URL}/api/dashboard/stats`, {
          cache: 'no-store'
        })

        if (res.ok) {
          stopped = true
          clearInterval(timer)
          clearTimeout(retryTimer)

          setStatus('ready')

          setTimeout(() => {
            if (onReady) onReady()
          }, 300)

          return
        }
      } catch (e) {
        console.log('Ping failed')
      }

      retryTimer = setTimeout(checkServer, 3000)
    }

    checkServer()

    return () => {
      stopped = true
      clearInterval(timer)
      clearTimeout(retryTimer)
    }
  }, [onReady])

  return (
    <div
      style={{
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'sans-serif',
        gap: 12
      }}
    >
      {/* Spinner */}
      <div
        style={{
          width: 30,
          height: 30,
          border: '4px solid #ddd',
          borderTop: '4px solid #333',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }}
      />

      {/* Loading */}
      {status === 'loading' && (
        <>
          <p>Backend is starting... please wait</p>
          <small>Free tier cold start (~30–60s) • {time}s</small>
        </>
      )}

      {/* Ready */}
      {status === 'ready' && <p>Loading app...</p>}

      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}
