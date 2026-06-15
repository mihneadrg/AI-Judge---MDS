function VerdictDisplay({ verdict, onNewCase, hideButton = false }) {
    return (
        <div className="bg-gradient-to-br from-amber-50 via-amber-100 to-amber-200 rounded-lg shadow-2xl border-4 border-amber-700 p-8">
            <div className="text-center mb-8 pb-6 border-b-4 border-double border-amber-800">
                <div className="text-6xl mb-3">⚖️</div>
                <h2 className="text-4xl font-serif font-black text-amber-900 uppercase tracking-widest mb-2">
                    Verdict Oficial
                </h2>
                <p className="text-amber-700 font-legal italic text-sm">
                    Issued by The Dramatic AI Court • {new Date().toLocaleDateString('ro-RO')}
                </p>
            </div>

            <div className="mb-6 bg-amber-900 text-amber-50 p-4 rounded-lg shadow-inner">
                <h3 className="text-2xl font-serif font-bold text-center">
                    {verdict.case_title}
                </h3>
            </div>

            <Section title="⚠️ Acuzații" content={verdict.charges} />
            <Section title="🔍 Dovezi Prezentate" content={verdict.evidence_presented} />
            <Section title="📚 Precedent Legal" content={verdict.legal_precedent} />

            <div className="my-8 bg-gradient-to-r from-red-100 via-amber-100 to-red-100 border-4 border-red-700 rounded-lg p-6 shadow-2xl">
                <h3 className="text-3xl font-serif font-black text-red-900 uppercase text-center mb-3 tracking-widest">
                    🔨 Verdict
                </h3>
                <p className="text-5xl font-serif font-black text-center text-red-800">
                    {verdict.verdict}
                </p>
            </div>

            <div className="mb-6 bg-amber-200 border-l-8 border-amber-800 p-6 rounded shadow-lg">
                <h3 className="text-2xl font-serif font-bold text-amber-900 mb-3 flex items-center">
                    ⚖️ Sentința
                </h3>
                <p className="text-xl font-legal text-amber-900 leading-relaxed">
                    {verdict.sentence}
                </p>
            </div>

            <Section title="📖 Motivare Juridică" content={verdict.legal_reasoning} />

            <div className="mt-8 bg-gradient-to-r from-amber-800 to-amber-900 text-amber-50 p-6 rounded-lg shadow-xl">
                <h3 className="text-xl font-serif font-bold mb-3 text-center">
                    💬 Cuvintele Finale ale Instanței
                </h3>
                <p className="text-lg font-legal italic text-center leading-relaxed">
                    "{verdict.courts_final_words}"
                </p>
            </div>

            <div className="mt-8 pt-6 border-t-2 border-amber-700 flex justify-between items-center">
                <div className="text-amber-700 font-legal italic">
                    <p className="font-bold">The Dramatic AI Judge</p>
                    <p className="text-sm">Presiding Officer</p>
                </div>
                <div className="text-6xl opacity-20 transform rotate-12">⚖️</div>
            </div>

            {!hideButton && (
                <button
                    onClick={onNewCase}
                    className="mt-8 w-full bg-amber-700 hover:bg-amber-800 text-amber-50 font-serif font-bold
                     py-4 px-6 rounded-lg shadow-lg uppercase tracking-wider text-lg
                     transform transition hover:scale-105 active:scale-95"
                >
                    📋 Depune un Caz Nou
                </button>
            )}
        </div>
    )
}

function Section({ title, content }) {
    return (
        <div className="mb-6">
            <h3 className="text-xl font-serif font-bold text-amber-900 mb-2 flex items-center">
                {title}
            </h3>
            <p className="text-lg font-legal text-amber-800 leading-relaxed pl-4 border-l-4 border-amber-400">
                {content}
            </p>
        </div>
    )
}

export default VerdictDisplay