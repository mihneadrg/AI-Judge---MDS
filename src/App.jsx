import { useState } from 'react'
import ModeSelector from './components/ModeSelector'
import ComplaintForm from './components/ComplaintForm'
import QuestionForm from './components/QuestionForm'
import VerdictDisplay from './components/VerdictDisplay'
import CourtroomView from './components/CourtroomView'

// Stările aplicației:
// "mode-select" → selectezi modul
// "form"        → userul descrie situația (modul participă)
// "question"    → agentul pune o întrebare (modul participă)
// "loading"     → se procesează (modul participă)
// "verdict"     → verdictul e gata (modul participă)
// "courtroom"   → camera live non-stop (modul watch)

function App() {
  const [appState, setAppState] = useState('mode-select')
  const [sessionId, setSessionId] = useState(null)
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [questionsAsked, setQuestionsAsked] = useState(0)
  const [verdict, setVerdict] = useState(null)
  const [error, setError] = useState(null)

  // ── Modul Participă ───────────────────────────────────────────────────────

  const handleSubmitSituation = async (situation) => {
    setError(null)
    setAppState('loading')
    try {
      const response = await fetch('http://localhost:8000/api/v1/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ situation }),
      })
      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || 'A apărut o eroare')
      }
      handlePipelineResponse(await response.json())
    } catch (err) {
      setError(err.message)
      setAppState('form')
    }
  }

  const handleAnswerQuestion = async (answer) => {
    setError(null)
    setAppState('loading')
    try {
      const response = await fetch('http://localhost:8000/api/v1/answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, answer }),
      })
      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || 'A apărut o eroare')
      }
      handlePipelineResponse(await response.json())
    } catch (err) {
      setError(err.message)
      setAppState('question')
    }
  }

  const handlePipelineResponse = (data) => {
    if (data.state === 'question') {
      setSessionId(data.session_id)
      setCurrentQuestion(data.question)
      setQuestionsAsked(data.questions_asked)
      setAppState('question')
    } else if (data.state === 'verdict') {
      setVerdict({ ...data.verdict.final_verdict, legal_article: data.verdict.legal_article })
      setAppState('verdict')
    } else if (data.state === 'error') {
      setError(data.error)
      setAppState('form')
    }
  }

  // ── Reset ─────────────────────────────────────────────────────────────────

  const handleNewCase = () => {
    setAppState('mode-select')
    setSessionId(null)
    setCurrentQuestion(null)
    setQuestionsAsked(0)
    setVerdict(null)
    setError(null)
  }

  // ── Render ────────────────────────────────────────────────────────────────

  const inCourtroom = appState === 'courtroom'

  return (
    <div className="min-h-screen py-12 px-4">
      <div className={`mx-auto ${inCourtroom ? 'max-w-4xl' : 'max-w-4xl'}`}>

        {/* Header — mai compact în modul cameră */}
        <header className={`text-center ${inCourtroom ? 'mb-4' : 'mb-12'}`}>
          <div className="inline-block">
            <h1 className={`font-serif font-bold text-amber-400 tracking-wide
              ${inCourtroom ? 'text-2xl mb-1' : 'text-5xl mb-2'}`}>
              ⚖️ THE DRAMATIC AI JUDGE
            </h1>
            {!inCourtroom && (
              <>
                <div className="h-1 bg-gradient-to-r from-transparent via-amber-400 to-transparent" />
                <p className="text-amber-100 mt-4 text-lg font-legal italic">
                  "Where everyday disputes meet theatrical justice"
                </p>
              </>
            )}
          </div>
        </header>

        {/* Indicator de progres (modul participă) */}
        {(appState === 'question' || appState === 'loading') && (
          <ProgressIndicator appState={appState} questionsAsked={questionsAsked} />
        )}

        {/* Conținut principal */}
        {appState === 'mode-select' && (
          <>
            {error && (
              <div className="mb-6 bg-red-100 border-2 border-red-500 text-red-800 px-4 py-3 rounded font-legal text-center">
                {error}
              </div>
            )}
            <ModeSelector
              onSelectParticipate={() => { setError(null); setAppState('form') }}
              onSelectWatch={() => { setError(null); setAppState('courtroom') }}
            />
          </>
        )}

        {appState === 'form' && (
          <ComplaintForm onSubmit={handleSubmitSituation} error={error} />
        )}

        {appState === 'loading' && (
          <LoadingScreen questionsAsked={questionsAsked} />
        )}

        {appState === 'question' && (
          <QuestionForm
            question={currentQuestion}
            questionsAsked={questionsAsked}
            onAnswer={handleAnswerQuestion}
            error={error}
          />
        )}

        {appState === 'verdict' && (
          <VerdictDisplay verdict={verdict} onNewCase={handleNewCase} />
        )}

        {appState === 'courtroom' && (
          <CourtroomView onExit={handleNewCase} />
        )}

      </div>
    </div>
  )
}

// ── Sub-componente ─────────────────────────────────────────────────────────

function ProgressIndicator({ appState, questionsAsked }) {
  const steps = [
    { label: 'Reclamație', done: true },
    { label: `Interogatoriu (${questionsAsked}/3)`, done: false, active: appState === 'question' || appState === 'loading' },
    { label: 'Verdict', done: false },
  ]
  return (
    <div className="flex items-center justify-center mb-8 gap-2">
      {steps.map((step, i) => (
        <div key={i} className="flex items-center gap-2">
          <div className={`px-3 py-1 rounded-full text-sm font-serif border-2 transition-all
            ${step.done ? 'bg-amber-600 border-amber-600 text-white' :
              step.active ? 'bg-amber-900 border-amber-400 text-amber-300 animate-pulse' :
              'bg-transparent border-amber-800 text-amber-700'}`}>
            {step.label}
          </div>
          {i < steps.length - 1 && (
            <div className={`w-8 h-0.5 ${step.done ? 'bg-amber-500' : 'bg-amber-800'}`} />
          )}
        </div>
      ))}
    </div>
  )
}

function LoadingScreen({ questionsAsked }) {
  const message = questionsAsked > 0
    ? 'Curtea analizează răspunsurile...'
    : 'Curtea examinează cazul...'
  return (
    <div className="bg-gradient-to-br from-amber-50 to-amber-100 rounded-lg shadow-2xl border-4 border-amber-600 p-12 text-center">
      <div className="text-6xl mb-6 animate-bounce">⚖️</div>
      <h2 className="text-2xl font-serif font-bold text-amber-900 mb-4">{message}</h2>
      <p className="text-amber-700 font-legal italic mb-8">Agenții AI deliberează... Vă rugăm să așteptați.</p>
      <div className="flex justify-center gap-2">
        {[0, 1, 2].map(i => (
          <div key={i} className="w-3 h-3 bg-amber-600 rounded-full animate-bounce"
            style={{ animationDelay: `${i * 0.15}s` }} />
        ))}
      </div>
    </div>
  )
}

export default App
