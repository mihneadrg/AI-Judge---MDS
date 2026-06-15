function ModeSelector({ onSelectParticipate, onSelectWatch }) {
  return (
    <div className="bg-gradient-to-br from-amber-50 to-amber-100 rounded-lg shadow-2xl border-4 border-amber-700 p-10">
      <div className="text-center mb-10">
        <p className="text-amber-800 font-legal text-xl italic">
          Cum doriți să participați la procesul de astăzi?
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Modul Participare */}
        <button
          onClick={onSelectParticipate}
          className="group relative bg-gradient-to-br from-amber-700 to-amber-900
                     hover:from-amber-600 hover:to-amber-800
                     text-amber-50 rounded-lg p-8 shadow-xl border-2 border-amber-500
                     transform transition-all duration-200 hover:scale-105 active:scale-95
                     text-left"
        >
          <div className="text-5xl mb-4">📜</div>
          <h2 className="text-2xl font-serif font-bold mb-3 uppercase tracking-wide">
            Participă la Proces
          </h2>
          <p className="font-legal text-amber-200 text-sm leading-relaxed">
            Tu ești reclamantul. Descrie situația, răspunde la întrebările
            inchizitorului și primești verdictul.
          </p>
          <div className="mt-6 flex items-center gap-2 text-amber-300 text-sm font-legal">
            <span>👤</span>
            <span>TU joci rolul reclamantului</span>
          </div>
          <div className="absolute bottom-4 right-4 text-amber-500 text-2xl
                          opacity-0 group-hover:opacity-100 transition-opacity">
            →
          </div>
        </button>

        {/* Modul Watch */}
        <button
          onClick={onSelectWatch}
          className="group relative bg-gradient-to-br from-slate-700 to-slate-900
                     hover:from-slate-600 hover:to-slate-800
                     text-slate-50 rounded-lg p-8 shadow-xl border-2 border-slate-500
                     transform transition-all duration-200 hover:scale-105 active:scale-95
                     text-left"
        >
          <div className="text-5xl mb-4">🎭</div>
          <h2 className="text-2xl font-serif font-bold mb-3 uppercase tracking-wide">
            Urmărește un Proces
          </h2>
          <p className="font-legal text-slate-300 text-sm leading-relaxed">
            Toți agenții AI joacă singuri. Tu ești spectator la un proces
            generat complet automat de inteligența artificială.
          </p>
          <div className="mt-6 flex items-center gap-2 text-slate-400 text-sm font-legal">
            <span>🤖</span>
            <span>AI joacă toate rolurile</span>
          </div>
          <div className="absolute bottom-4 right-4 text-slate-400 text-2xl
                          opacity-0 group-hover:opacity-100 transition-opacity">
            →
          </div>
        </button>
      </div>

      <div className="mt-8 text-center text-amber-600 font-legal text-sm italic">
        "Curtea Dramatică AI este în sesiune permanentă"
      </div>
    </div>
  )
}

export default ModeSelector
