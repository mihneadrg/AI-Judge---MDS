import { useState, useEffect, useRef } from 'react'

function QuestionForm({ question, questionsAsked, onAnswer, error }) {
  const [answer, setAnswer] = useState('')
  const textareaRef = useRef(null)

  // Focus automat pe textarea când apare o nouă întrebare
  useEffect(() => {
    setAnswer('')
    if (textareaRef.current) {
      textareaRef.current.focus()
    }
  }, [question])

  const handleSubmit = (e) => {
    e.preventDefault()
    const trimmed = answer.trim()
    if (!trimmed) return
    onAnswer(trimmed)
  }

  const isValid = answer.trim().length > 0

  return (
    <div className="bg-gradient-to-br from-amber-50 to-amber-100 rounded-lg shadow-2xl border-4 border-amber-700 p-8">

      {/* Header interogatoriu */}
      <div className="text-center mb-6 pb-4 border-b-2 border-amber-800">
        <div className="text-4xl mb-2">🔍</div>
        <h2 className="text-2xl font-serif font-bold text-amber-900 uppercase tracking-widest">
          Interogatoriu
        </h2>
        <p className="text-amber-600 text-sm mt-1 font-legal italic">
          Întrebarea {questionsAsked + 1} din maxim 3
        </p>
      </div>

      {/* Bule de progres */}
      <div className="flex justify-center gap-3 mb-6">
        {[1, 2, 3].map(i => (
          <div
            key={i}
            className={`w-8 h-8 rounded-full border-2 flex items-center justify-center text-sm font-bold font-serif
              ${i <= questionsAsked ? 'bg-amber-700 border-amber-700 text-white' :
                i === questionsAsked + 1 ? 'bg-amber-200 border-amber-700 text-amber-900 ring-2 ring-amber-400 ring-offset-1' :
                'bg-transparent border-amber-300 text-amber-400'}`}
          >
            {i <= questionsAsked ? '✓' : i}
          </div>
        ))}
      </div>

      {/* Întrebarea agentului — stilizată ca o bulă de chat */}
      <div className="mb-6">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 bg-amber-800 rounded-full flex items-center justify-center text-xl flex-shrink-0 mt-1">
            👨‍⚖️
          </div>
          <div className="bg-amber-800 text-amber-50 rounded-lg rounded-tl-none p-4 shadow-lg flex-1">
            <p className="text-sm font-bold text-amber-300 mb-1 uppercase tracking-wider">
              Court Inquisitor Severus
            </p>
            <p className="font-legal text-lg leading-relaxed">
              {question}
            </p>
          </div>
        </div>
      </div>

      {/* Input răspuns */}
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-amber-900 font-serif font-semibold mb-2">
            Răspunsul dumneavoastră:
          </label>
          <textarea
            ref={textareaRef}
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Răspundeți onest — curtea vede totul..."
            rows={4}
            maxLength={500}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && e.ctrlKey) handleSubmit(e)
            }}
            className="w-full px-4 py-3 border-2 border-amber-700 rounded bg-amber-50
                       font-legal text-gray-800 placeholder-amber-400
                       focus:outline-none focus:ring-2 focus:ring-amber-500
                       resize-none"
          />
          <div className="flex justify-between mt-1 text-xs text-amber-600 font-legal">
            <span>{answer.length}/500 caractere</span>
            <span className="italic">Ctrl+Enter pentru a trimite</span>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-100 border-l-4 border-red-600 text-red-800 font-legal text-sm">
            <strong>⚠️ Eroare:</strong> {error}
          </div>
        )}

        <button
          type="submit"
          disabled={!isValid}
          className="w-full bg-amber-700 hover:bg-amber-800 text-amber-50 font-serif font-bold
                     py-4 px-6 rounded-lg shadow-lg uppercase tracking-wider text-lg
                     disabled:opacity-50 disabled:cursor-not-allowed
                     transform transition hover:scale-105 active:scale-95"
        >
          📜 Depun Mărturie
        </button>
      </form>

      {/* Footer */}
      <div className="mt-4 pt-3 border-t border-amber-300 text-center text-xs text-amber-600 font-legal italic">
        Orice declarație falsă poate agrava sentința finală.
      </div>
    </div>
  )
}

export default QuestionForm
