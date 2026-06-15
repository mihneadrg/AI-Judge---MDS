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

        {/* Modul Cameră Live */}
        <button
          onClick={onSelectWatch}
          className="group relative bg-gradient-to-br from-slate-800 to-slate-950
                     hover:from-slate-700 hover:to-slate-900
                     text-slate-50 rounded-lg p-8 shadow-xl border-2 border-slate-500
                     hover:border-red-500
                     transform transition-all duration-200 hover:scale-105 active:scale-95
                     text-left overflow-hidden"
        >
          {/* Badge LIVE */}
          <div className="absolute top-4 right-4 flex items-center gap-1.5
                          bg-red-700 text-white px-2 py-0.5 rounded-full text-xs font-bold uppercase tracking-widest">
            <span className="relative flex h-1.5 w-1.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75" />
              <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-white" />
            </span>
            LIVE
          </div>

          <div className="text-5xl mb-4">🎭</div>
          <h2 className="text-2xl font-serif font-bold mb-3 uppercase tracking-wide">
            Camera Tribunalului
          </h2>
          <p className="font-legal text-slate-300 text-sm leading-relaxed">
            Intră live în sala de tribunal. Procese generate complet de AI
            se desfășoară non-stop, unul după altul.
          </p>
          <div className="mt-6 flex items-center gap-2 text-slate-400 text-sm font-legal">
            <span>🤖</span>
            <span>AI joacă toate rolurile • Non-stop</span>
          </div>
          <div className="absolute bottom-4 right-4 text-slate-500 text-2xl
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
