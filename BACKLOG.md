# 📋 Backlog Proiect - The Dramatic AI Judge

---

## 🚀 Epic 1: Arhitectură, Setup și Infrastructură Bază

Acest epic se concentrează pe fundația tehnică a proiectului, pregătind mediul de dezvoltare în Python și stabilind arhitectura.

### [US-1.1] Configurare Mediu de Dezvoltare

**User Story:** Ca utilizator, vreau să accesez o aplicație construită pe o fundație stabilă și sigură, astfel încât experiența mea să nu fie întreruptă de erori interne sau probleme de sistem.

**Criterii de Acceptanță:**
- Există un fișier `requirements.txt` sau `pyproject.toml`.
- Fișierul `.gitignore` exclude fișierele specifice sistemului de operare și directoarele `.env` sau `venv/`.
- Structura proiectului separă clar logica sursă (`src/`) de teste (`tests/`).

---

### [US-1.2] Setup Endpoint-uri API (Backend)

**User Story:** Ca utilizator, vreau ca textul plângerii mele să fie preluat și transmis rapid către instanța AI, astfel încât să poată fi analizat fără ca datele mele să se piardă.

**Criterii de Acceptanță:**
- Serverul pornește fără erori pe localhost.
- Un request de test către endpoint returnează codul HTTP 200 OK.

---

## 🧠 Epic 2: Core AI Logic & Prompt Engineering

Aici este implementată inima aplicației: comunicarea cu modelul de limbaj și aplicarea "persona-ului" de judecător dramatic.

### [US-2.1] Integrare Client LLM

**User Story:** Ca utilizator, vreau ca aplicația să fie mereu conectată la "creierul" judecătorului AI, astfel încât să îmi primesc verdictul rapid, fără întârzieri sau erori de conexiune.

**Criterii de Acceptanță:**
- Cheia API este citită dintr-un fișier `.env` (niciodată hardcodată).
- Există un mecanism de try-catch pentru a gestiona erorile de rețea sau de autentificare cu API-ul.

---

### [US-2.2] Procesarea Situației prin "The Judge Persona"

**User Story:** Ca utilizator, vreau ca situația mea cotidiană să fie analizată printr-un filtru teatral specific, astfel încât rezultatul să fie o judecată completă și amuzantă.

**Criterii de Acceptanță:**
- Sistemul injectează input-ul utilizatorului în system prompt-ul predefinit ("Act as a dramatic judge...").
- Output-ul de la LLM conține obligatoriu cele 8 câmpuri cerute: Case Title, Charges, Evidence Presented, Legal Precedent, VERDICT, Sentence, Legal Reasoning, Court's Final Words.

---

### [US-2.3] Parsarea și Structurarea Output-ului

**User Story:** Ca utilizator, vreau ca decizia judecătorului să fie organizată logic în fundal, astfel încât să o pot citi ulterior sub forma unui document structurat, fără ca vreo informație să fie omisă sau amestecată.

**Criterii de Acceptanță:**
- Se folosește un parser cu expresii regulate (Regex) sau un structured output format nativ al LLM-ului pentru a separa câmpurile.
- Dacă LLM-ul omite o secțiune, sistemul returnează un mesaj de eroare grațios sau o valoare default ("N/A").

---

## 🎭 Epic 3: Sistem de Interogatoriu Multi-Turn

Acest epic acoperă funcționalitatea de conversație între utilizator și agentul interogator, care clarifică detaliile cazului înainte de verdict.

### [US-3.1] Inițierea Sesiunii de Interogatoriu

**User Story:** Ca utilizator, vreau ca după ce descriu situația să fiu întrebat de un agent AI pentru detalii suplimentare, astfel încât verdictul final să fie cât mai personalizat și specific cazului meu.

**Criterii de Acceptanță:**
- La trimiterea situației, sistemul creează o sesiune unică identificată printr-un `session_id`.
- Dacă agentul interogator consideră că are nevoie de mai multe informații, returnează o întrebare specifică (nu generică) legată de situația descrisă.
- Dacă situația este deja suficient de detaliată, sistemul sare direct la verdict.

---

### [US-3.2] Dialogul cu Agentul Interogator

**User Story:** Ca utilizator, vreau să răspund la întrebările agentului una câte una, astfel încât să simt că particip activ la procesul de judecată, ca într-un tribunal real.

**Criterii de Acceptanță:**
- Agentul pune maximum 3 întrebări per sesiune.
- Fiecare întrebare apare individual, într-o bulă de chat cu identitatea vizuală a "Court Inquisitor Severus".
- Utilizatorul poate trimite răspunsul prin buton sau Ctrl+Enter.
- Progresul interogatoriului (ex: "Întrebarea 2 din 3") este vizibil.

---

### [US-3.3] Transmiterea Contextului Complet către Agenții de Judecată

**User Story:** Ca utilizator, vreau ca răspunsurile mele din interogatoriu să fie luate în considerare în verdict, astfel încât judecata să reflecte toate detaliile pe care le-am furnizat, nu doar descrierea inițială.

**Criterii de Acceptanță:**
- Toate perechile întrebare-răspuns din interogatoriu sunt concatenate cu situația inițială și transmise către ProsecutorAgent.
- Dovezile prezentate în verdict conțin informații din răspunsurile utilizatorului, nu doar din descrierea inițială.
- Sesiunea este ștearsă din memorie după pronunțarea verdictului.

---

### [US-3.4] Gestionarea Erorilor în Sesiunea de Interogatoriu

**User Story:** Ca utilizator, vreau ca aplicația să nu se blocheze dacă sesiunea mea expiră sau dacă apare o eroare în timpul interogatoriului, astfel încât să pot relua procesul fără frustrare.

**Criterii de Acceptanță:**
- Dacă `session_id`-ul nu există sau a expirat, sistemul returnează un mesaj de eroare clar (HTTP 503 cu detalii).
- Dacă agentul interogator nu generează JSON valid, sistemul procedează direct la verdict cu informațiile disponibile.
- Utilizatorul vede un mesaj de eroare prietenos pe frontend, nu un crash al aplicației.

---

## 🖥️ Epic 4: Interacțiunea cu Utilizatorul (Interfață)

Acest epic definește modul în care utilizatorul final introduce datele și citește rezultatul.

### [US-4.1] Formularul de Reclamație

**User Story:** Ca utilizator, vreau să am la dispoziție un câmp de text clar unde să descriu situația, astfel încât să pot trimite ușor cazul meu instanței AI.

**Criterii de Acceptanță:**
- Input-ul acceptă texte de până la 1000 de caractere.
- Nu se pot trimite cereri goale (validare pe frontend/backend).

---

### [US-4.2] Afișarea Verdictului Teatral

**User Story:** Ca utilizator, vreau să văd răspunsul împărțit clar pe categorii cu un design ce amintește de un document legal, astfel încât să fie imersiv și ușor de citit.

**Criterii de Acceptanță:**
- Fiecare dintre cele 8 câmpuri (Case Title, Charges etc.) este afișat distinct (ex: cu bold sau ca titlu de secțiune).
- Verdictul final și Sentința sunt evidențiate vizual.

---

## 🛡️ Epic 5: Quality Assurance & Error Handling

Asigurarea robusteței aplicației.

### [US-5.1] Validarea Textului de Intrare

**User Story:** Ca utilizator, vreau ca platforma să îmi verifice input-ul înainte de trimitere, astfel încât să fiu avertizat dacă am introdus date invalide și platforma să rămână sigură pentru toți.

**Criterii de Acceptanță:**
- Input-ul este sanitizat înainte de a fi trimis către LLM.

---

### [US-5.2] Teste Unitare pentru Parser-ul de Output

**User Story:** Ca utilizator, vreau ca aplicația să îmi ofere o experiență fluidă și să nu se blocheze (să nu dea crash) chiar și atunci când judecătorul AI este "confuz" și formulează greșit răspunsul.

**Criterii de Acceptanță:**
- Există cel puțin un test case pentru un răspuns ideal, formatat perfect de LLM.
- Există cel puțin un test case pentru un răspuns parțial sau greșit formatat de LLM.

---

## 🎭 Epic 6: Modul Watch — Proces Complet Automat între Agenți ✅

Acest epic introduce un mod de vizionare în care toți actorii procesului (inclusiv reclamantul) sunt jucați de agenți AI, fără niciun input uman. Utilizatorul este spectator.

### [US-6.1] Selectorul de Mod ✅

**User Story:** Ca utilizator, vreau să aleg la pornire între a participa la proces sau a urmări un proces generat complet de AI, astfel încât să pot experimenta ambele perspective.

**Criterii de Acceptanță:**
- La deschiderea aplicației apare un ecran de selectare cu două opțiuni clare.
- "Participă la Proces" pornește fluxul existent (utilizatorul introduce plângerea).
- "Urmărește un Proces" declanșează modul complet automat.
- Ambele moduri revin la ecranul de selecție după finalizarea procesului.

**Implementare:** `ModeSelector.jsx`, stare `mode-select` în `App.jsx`.

---

### [US-6.2] Agentul Reclamant (ComplainantAgent) ✅

**User Story:** Ca spectator, vreau ca reclamantul să fie jucat de un agent AI care generează o situație coerentă și răspunde consistent la întrebări, astfel încât procesul să fie credibil și amuzant fără input uman.

**Criterii de Acceptanță:**
- `ComplainantAgent` generează o plângere aleatorie cu detalii specifice (nume, loc, timp, context).
- Agentul răspunde la întrebările Interogatorului rămânând în personaj și fără să se contrazică.
- Există un răspuns fallback dacă parsarea JSON eșuează.

**Implementare:** `src/agents/complainant_agent.py`.

---

### [US-6.3] Pipeline Autonom (run_autonomous_trial) ✅

**User Story:** Ca spectator, vreau ca întregul ciclu al procesului să ruleze automat pe server, astfel încât să primesc un transcript complet cu toate intervențiile fiecărui agent.

**Criterii de Acceptanță:**
- Metoda `run_autonomous_trial()` orchestrează: ComplainantAgent → InterrogatorAgent (max 3 runde) → ComplainantAgent (răspunsuri) → ProsecutorAgent → JudgeAgent.
- Returnează un transcript JSON cu: `situation`, `complainant_name`, `interrogation[]`, `prosecution`, `final_verdict`, `processing_time_seconds`.
- Endpoint nou `POST /api/v1/watch` expune această funcționalitate.

**Implementare:** `CourtPipeline.run_autonomous_trial()` în `pipeline.py`, endpoint în `main.py`.

---

### [US-6.4] Afișarea Pas cu Pas a Procesului (TrialWatcher) ✅

**User Story:** Ca spectator, vreau să văd procesul desfășurându-se treptat, cu fiecare intervenție apărând pe rând, astfel încât să am senzația că urmăresc un proces în timp real.

**Criterii de Acceptanță:**
- Fiecare intervenție (reclamant, inchizitor, procuror, judecător) apare separat cu un delay de 2 secunde.
- Fiecare actor are un stil vizual distinct: reclamant (verde), inchizitor (violet), procuror (roșu), verdict (auriu).
- Un indicator "în desfășurare / încheiat" este vizibil pe tot parcursul.
- La final se afișează `VerdictDisplay` complet cu butonul de caz nou.

**Implementare:** `TrialWatcher.jsx`, animație `fadeIn` în `tailwind.config.js`.