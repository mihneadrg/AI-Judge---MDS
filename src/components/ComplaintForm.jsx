import { useState } from 'react'

function ComplaintForm({ onSubmit, isLoading, error }) {
    const [situation, setSituation] = useState('')
    const charLimit = 1000

    const handleSubmit = (e) => {
        e.preventDefault()
        const trimmed = situation.trim()
        if (trimmed.length === 0) return
        onSubmit(trimmed)
    }

    const isValid = situation.trim().length > 0 && situation.length <= charLimit

    return (
        <div className="bg-gradient-to-br from-amber-50 to-amber-100 rounded-lg shadow-2xl border-4 border-amber-600 p-8">
            <div className="text-center mb-6 pb-4 border-b-2 border-amber-800">
                <h2 className="text-2xl font-serif font-bold text-amber-900 uppercase tracking-widest">
                    📜 Formular de Reclamație
                </h2>
                <p className="text-amber-700 text-sm mt-2 font-legal italic">
                    Complaint Form № {Math.floor(Math.random() * 10000).toString().padStart(5, '0')}
                </p>
            </div>

            <form onSubmit={handleSubmit}>
                <div className="mb-6">
                    <label className="block text-amber-900 font-serif font-semibold mb-3 text-lg">
                        Descrieți situația dumneavoastră:
                    </label>
                    <textarea
                        value={situation}
                        onChange={(e) => setSituation(e.target.value)}
                        placeholder="Ex: Colegul meu a mâncat ultima felie de pizza fără să întrebe..."
                        maxLength={charLimit}
                        rows={8}
                        className="w-full px-4 py-3 border-2 border-amber-700 rounded bg-amber-50 
                     font-legal text-gray-800 placeholder-amber-400
                     focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent
                     resize-none"
                    />

                    <div className="flex justify-between items-center mt-2 text-sm">
                        <span className={`font-legal ${situation.length > charLimit ? 'text-red-600' : 'text-amber-600'}`}>
                            {situation.length} / {charLimit} caractere
                        </span>
                        {situation.trim().length === 0 && situation.length > 0 && (
                            <span className="text-red-600 font-legal italic">
                                Textul nu poate conține doar spații
                            </span>
                        )}
                    </div>
                </div>

                {error && (
                    <div className="mb-4 p-4 bg-red-100 border-l-4 border-red-600 text-red-800 font-legal">
                        <strong>⚠️ Eroare:</strong> {error}
                    </div>
                )}

                <button
                    type="submit"
                    disabled={!isValid || isLoading}
                    className="w-full bg-amber-700 hover:bg-amber-800 text-amber-50 font-serif font-bold 
                   py-4 px-6 rounded-lg shadow-lg uppercase tracking-wider text-lg
                   disabled:opacity-50 disabled:cursor-not-allowed
                   transform transition hover:scale-105 active:scale-95"
                >
                    {isLoading ? (
                        <span className="flex items-center justify-center">
                            <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Se analizează cazul...
                        </span>
                    ) : (
                        '⚖️ Trimite la Instanță'
                    )}
                </button>
            </form>

            <div className="mt-6 pt-4 border-t-2 border-amber-300 text-center text-xs text-amber-600 font-legal italic">
                Prin trimiterea acestui formular, acceptați jurisdicția instanței AI dramatice.
            </div>
        </div>
    )
}

export default ComplaintForm