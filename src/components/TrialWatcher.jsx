import { useState, useEffect } from 'react'
import VerdictDisplay from './VerdictDisplay'

// Construiește lista ordonată de pași din datele procesului
function buildSteps(trialData) {
  const steps = []

  steps.push({
    type: 'complainant',
    name: trialData.complainant_name,
    text: trialData.situation,
  })

  for (const { question, answer } of trialData.interrogation) {
    steps.push({ type: 'interrogator', text: question })
    steps.push({ type: 'complainant', name: trialData.complainant_name, text: answer })
  }

  steps.push({
    type: 'prosecutor',
    text: trialData.prosecution.prosecution_summary,
    charges: trialData.prosecution.formal_charges,
    severity: trialData.prosecution.severity_level,
  })

  steps.push({ type: 'verdict', verdict: trialData.final_verdict })

  return steps
}

// Delay între pași (ms)
const STEP_DELAY = 2000

function TrialWatcher({ trialData, onNewCase }) {
  const steps = buildSteps(trialData)
  const [visibleCount, setVisibleCount] = useState(0)

  useEffect(() => {
    if (visibleCount >= steps.length) return
    const timer = setTimeout(() => setVisibleCount(c => c + 1), STEP_DELAY)
    return () => clearTimeout(timer)
  }, [visibleCount, steps.length])

  const allVisible = visibleCount >= steps.length

  return (
    <div className="space-y-5">
      {/* Banner de stare */}
      <div className={`text-center py-2 px-4 rounded-full text-sm font-legal font-semibold mx-auto w-fit
        ${allVisible
          ? 'bg-amber-700 text-amber-50'
          : 'bg-slate-700 text-slate-200 animate-pulse'}`}>
        {allVisible ? '⚖️ Proces încheiat' : '🎭 Proces în desfășurare...'}
      </div>

      {/* Pași vizibili */}
      {steps.slice(0, visibleCount).map((step, i) => (
        <StepCard
          key={i}
          step={step}
          onNewCase={onNewCase}
          isLast={i === steps.length - 1}
        />
      ))}

      {/* Indicator "urmează..." */}
      {!allVisible && (
        <div className="flex items-center justify-center gap-3 py-4 text-amber-600 font-legal italic text-sm">
          <div className="flex gap-1">
            {[0, 1, 2].map(i => (
              <div
                key={i}
                className="w-2 h-2 bg-amber-500 rounded-full animate-bounce"
                style={{ animationDelay: `${i * 0.15}s` }}
              />
            ))}
          </div>
          <span>{nextActorLabel(steps[visibleCount])}</span>
        </div>
      )}
    </div>
  )
}

function nextActorLabel(step) {
  if (!step) return ''
  switch (step.type) {
    case 'complainant':  return 'Reclamantul pregătește declarația...'
    case 'interrogator': return 'Inchizitorul formulează întrebarea...'
    case 'prosecutor':   return 'Procurorul construiește dosarul...'
    case 'verdict':      return 'Judecătorul deliberează...'
    default: return ''
  }
}

function StepCard({ step, onNewCase, isLast }) {
  if (step.type === 'verdict') {
    return (
      <div className="animate-fadeIn">
        <VerdictDisplay verdict={step.verdict} onNewCase={onNewCase} />
      </div>
    )
  }

  const config = {
    complainant: {
      bg: 'from-emerald-50 to-emerald-100',
      border: 'border-emerald-600',
      header: 'bg-emerald-700',
      icon: '👤',
      label: step.name || 'Reclamant',
      align: 'mr-auto',
      maxW: 'max-w-2xl',
    },
    interrogator: {
      bg: 'from-purple-50 to-purple-100',
      border: 'border-purple-700',
      header: 'bg-purple-800',
      icon: '🔎',
      label: 'Inchizitor Severus',
      align: 'ml-auto',
      maxW: 'max-w-2xl',
    },
    prosecutor: {
      bg: 'from-red-50 to-red-100',
      border: 'border-red-700',
      header: 'bg-red-800',
      icon: '⚡',
      label: 'Procuror Maximus',
      align: 'mx-auto',
      maxW: 'max-w-3xl w-full',
    },
  }

  const c = config[step.type]

  return (
    <div className={`animate-fadeIn ${c.align} ${c.maxW}`}>
      <div className={`bg-gradient-to-br ${c.bg} rounded-lg shadow-lg border-2 ${c.border} overflow-hidden`}>
        {/* Header */}
        <div className={`${c.header} text-white px-4 py-2 flex items-center gap-2`}>
          <span className="text-lg">{c.icon}</span>
          <span className="font-serif font-bold text-sm uppercase tracking-wider">{c.label}</span>
        </div>

        {/* Body */}
        <div className="px-5 py-4">
          <p className="font-legal text-gray-800 leading-relaxed">{step.text}</p>

          {/* Acuzații listate (doar pentru procuror) */}
          {step.charges && step.charges.length > 0 && (
            <div className="mt-4 border-t border-red-200 pt-3">
              <p className="text-xs font-serif font-bold text-red-700 uppercase tracking-wider mb-2">
                Capete de acuzare:
              </p>
              <ul className="list-disc list-inside space-y-1">
                {step.charges.map((charge, i) => (
                  <li key={i} className="text-sm text-red-800 font-legal">{charge}</li>
                ))}
              </ul>
              {step.severity && (
                <span className={`inline-block mt-3 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider
                  ${step.severity === 'CATASTROPHIC' ? 'bg-red-900 text-white' :
                    step.severity === 'SEVERE' ? 'bg-red-700 text-white' :
                    step.severity === 'MODERATE' ? 'bg-orange-500 text-white' :
                    'bg-yellow-400 text-yellow-900'}`}>
                  Severitate: {step.severity}
                </span>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default TrialWatcher
