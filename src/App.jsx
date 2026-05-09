import { useState } from 'react'
import ComplaintForm from './components/ComplaintForm'
import QuestionForm from './components/QuestionForm'
import VerdictDisplay from './components/VerdictDisplay'

// Stările aplicației:
// "form"      → userul descrie situația
// "question"  → agentul pune o întrebare
// "loading"   → se procesează (Prosecutor + Judge)
// "verdict"   → verdictul e gata

function App() {
  const [appState, setAppState] = useState('form')
  const [sessionId, setSessionId] = useState(null)
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [questionsAsked, setQuestionsAsked] = useState(0)
  const [verdict, setVerdict] = useState(null)
  const [error, setError] = useState(null)

  // Userul trimite situația inițială
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

      const data = await response.json()
      handlePipelineResponse(data)

    } catch (err) {
      setError(err.message)
      setAppState('form')
    }
  }

  // Userul răspunde la o întrebare
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

      const data = await response.json()
      handlePipelineResponse(data)

    } catch (err) {
      setError(err.message)
      setAppState('question')
    }
  }

  // Procesează răspunsul de la pipeline (comun pentru /start și /answer)
  const handlePipelineResponse = (data) => {
    if (data.state === 'question') {
      setSessionId(data.session_id)
      setCurrentQuestion(data.question)
      setQuestionsAsked(data.questions_asked)
      setAppState('question')
    } else if (data.state === 'verdict') {
      setVerdict(data.verdict.final_verdict)
      setAppState('verdict')
    } else if (data.state === 'error') {
      setError(data.error)
      setAppState('form')
    }
  }

  const handleNewCase = () => {
    setAppState('form')
    setSessionId(null)
    setCurrentQuestion(null)
    setQuestionsAsked(0)
    setVerdict(null)
    setError(null)
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <header className="text-center mb-12">
          <div className="inline-block">
            <h1 className="text-5xl font-serif font-bold text-amber-400 mb-2 tracking-wide">
              ⚖️ THE DRAMATIC AI JUDGE
            </h1>
            <div className="h-1 bg-gradient-to-r from-transparent via-amber-400 to-transparent"></div>
          </div>
          <p className="text-amber-100 mt-4 text-lg font-legal italic">
            "Where everyday disputes meet theatrical justice"
          </p>
        </header>

        {/* Indicator de progres — vizibil când nu suntem pe form */}
        {appState !== 'form' && appState !== 'verdict' && (
          <ProgressIndicator appState={appState} questionsAsked={questionsAsked} />
        )}

        {/* Conținut principal în funcție de stare */}
        {appState === 'form' && (
          <ComplaintForm
            onSubmit={handleSubmitSituation}
            error={error}
          />
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
          <VerdictDisplay
            verdict={verdict}
            onNewCase={handleNewCase}
          />
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
      <h2 className="text-2xl font-serif font-bold text-amber-900 mb-4">
        {message}
      </h2>
      <p className="text-amber-700 font-legal italic mb-8">
        Agenții AI deliberează... Vă rugăm să așteptați.
      </p>
      <div className="flex justify-center gap-2">
        {[0, 1, 2].map(i => (
          <div
            key={i}
            className="w-3 h-3 bg-amber-600 rounded-full animate-bounce"
            style={{ animationDelay: `${i * 0.15}s` }}
          />
        ))}
      </div>
    </div>
  )
}

export default App
