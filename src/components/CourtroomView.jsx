import { useState, useEffect, useRef } from 'react'
import TrialWatcher from './TrialWatcher'

const COUNTDOWN_SEC = 8

function CourtroomView({ onExit }) {
  const [phase, setPhase] = useState('loading')  // loading | watching | countdown
  const [trialData, setTrialData] = useState(null)
  const [trialNumber, setTrialNumber] = useState(1)
  const [countdown, setCountdown] = useState(COUNTDOWN_SEC)
  const [error, setError] = useState(null)
  const mountedRef = useRef(true)

  useEffect(() => {
    return () => { mountedRef.current = false }
  }, [])

  async function fetchTrial() {
    if (!mountedRef.current) return
    setPhase('loading')
    setError(null)
    try {
      const res = await fetch('http://localhost:8000/api/v1/watch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Eroare la generarea procesului')
      }
      const data = await res.json()
      if (!mountedRef.current) return
      setTrialData(data)
      setPhase('watching')
    } catch (err) {
      if (!mountedRef.current) return
      setError(err.message)
      setCountdown(COUNTDOWN_SEC)
      setPhase('countdown')
    }
  }

  // Prima încărcare
  useEffect(() => { fetchTrial() }, [])

  // Countdown între procese
  useEffect(() => {
    if (phase !== 'countdown') return
    if (countdown <= 0) {
      setTrialNumber(n => n + 1)
      fetchTrial()
      return
    }
    const timer = setTimeout(() => setCountdown(c => c - 1), 1000)
    return () => clearTimeout(timer)
  }, [phase, countdown])

  function handleTrialComplete() {
    setCountdown(COUNTDOWN_SEC)
    setPhase('countdown')
  }

  function handleSkip() {
    setCountdown(0)
  }

  return (
    <div>
      {/* Bara de sus */}
      <div className="flex items-center justify-between mb-6 px-1">
        <div className="flex items-center gap-3">
          {/* Badge LIVE */}
          <div className="flex items-center gap-2 bg-red-700 text-white px-3 py-1 rounded-full text-xs font-bold uppercase tracking-widest">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-white" />
            </span>
            LIVE
          </div>
          <span className="text-slate-300 font-serif font-bold text-sm uppercase tracking-wide">
            Camera Tribunalului
          </span>
          <span className="text-amber-400 font-legal text-sm">
            · Procesul #{trialNumber}
          </span>
        </div>

        <button
          onClick={onExit}
          className="text-slate-500 hover:text-slate-200 border border-slate-700
                     hover:border-slate-400 px-3 py-1 rounded text-sm font-legal transition-all"
        >
          ✕ Ieși din Curte
        </button>
      </div>

      {/* Conținut principal */}
      {phase === 'loading' && (
        <LoadingNextTrial trialNumber={trialNumber} />
      )}

      {phase === 'watching' && trialData && (
        <TrialWatcher
          trialData={trialData}
          isCourtroom
          onComplete={handleTrialComplete}
        />
      )}

      {phase === 'countdown' && (
        <BetweenTrials
          countdown={countdown}
          nextNumber={trialNumber + 1}
          error={error}
          onSkip={handleSkip}
        />
      )}
    </div>
  )
}

// ── Sub-componente ─────────────────────────────────────────────────────────

function LoadingNextTrial({ trialNumber }) {
  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg
                    border-2 border-slate-600 p-16 text-center shadow-2xl">
      <div className="text-6xl mb-5 animate-pulse">🎭</div>
      <h2 className="text-slate-100 font-serif text-2xl font-bold mb-2">
        Procesul #{trialNumber} se pregătește
      </h2>
      <p className="text-slate-400 font-legal text-sm mb-8">
        Agenții AI redactează cazul, formulează acuzațiile și deliberează...
      </p>
      <div className="flex justify-center gap-2">
        {[0, 1, 2].map(i => (
          <div
            key={i}
            className="w-3 h-3 bg-slate-500 rounded-full animate-bounce"
            style={{ animationDelay: `${i * 0.15}s` }}
          />
        ))}
      </div>
      <p className="text-slate-600 font-legal text-xs mt-8 italic">
        Poate dura 20-40 de secunde
      </p>
    </div>
  )
}

function BetweenTrials({ countdown, nextNumber, error, onSkip }) {
  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg
                    border-2 border-slate-600 p-16 text-center shadow-2xl">
      {error ? (
        <>
          <div className="text-5xl mb-4">⚠️</div>
          <p className="text-red-400 font-legal mb-2">Eroare la generare:</p>
          <p className="text-red-300 font-legal text-sm mb-6">{error}</p>
          <p className="text-slate-400 font-legal text-sm">Se reîncearcă în...</p>
        </>
      ) : (
        <>
          <div className="text-5xl mb-4">⚖️</div>
          <h2 className="text-slate-100 font-serif text-2xl font-bold mb-2">
            Proces încheiat!
          </h2>
          <p className="text-slate-400 font-legal text-sm mb-6">
            Procesul #{nextNumber} începe în...
          </p>
        </>
      )}

      {/* Countdown circular */}
      <div className="relative inline-flex items-center justify-center w-24 h-24 mb-6">
        <svg className="absolute w-24 h-24 -rotate-90" viewBox="0 0 96 96">
          <circle cx="48" cy="48" r="40" fill="none" stroke="#334155" strokeWidth="6" />
          <circle
            cx="48" cy="48" r="40" fill="none"
            stroke="#f59e0b" strokeWidth="6"
            strokeDasharray={`${2 * Math.PI * 40}`}
            strokeDashoffset={`${2 * Math.PI * 40 * (1 - countdown / COUNTDOWN_SEC)}`}
            strokeLinecap="round"
            style={{ transition: 'stroke-dashoffset 0.9s linear' }}
          />
        </svg>
        <span className="text-3xl font-serif font-black text-amber-400">{countdown}</span>
      </div>

      <div>
        <button
          onClick={onSkip}
          className="text-slate-400 hover:text-amber-300 text-sm font-legal
                     underline transition-colors"
        >
          Sari direct la procesul #{nextNumber} →
        </button>
      </div>
    </div>
  )
}

export { COUNTDOWN_SEC }
export default CourtroomView
