import { useState } from 'react'
import ComplaintForm from './components/ComplaintForm'
import VerdictDisplay from './components/VerdictDisplay'

function App() {
  const [verdict, setVerdict] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (situation) => {
    setIsLoading(true)
    setError(null)
    setVerdict(null)

    try {
      const response = await fetch('http://localhost:8000/api/v1/judge', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ situation }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to get judgment')
      }

      const data = await response.json()
      setVerdict(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleNewCase = () => {
    setVerdict(null)
    setError(null)
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
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

        {!verdict ? (
          <ComplaintForm
            onSubmit={handleSubmit}
            isLoading={isLoading}
            error={error}
          />
        ) : (
          <VerdictDisplay
            verdict={verdict}
            onNewCase={handleNewCase}
          />
        )}
      </div>
    </div>
  )
}

export default App