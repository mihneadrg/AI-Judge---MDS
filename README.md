# ⚖️ The Dramatic AI Judge

O aplicație web de tip "AI-First" bazată pe o arhitectură multi-agent autonomă. Proiectul preia dispute cotidiene sau neînțelegeri mărunte din viața de zi cu zi și le transformă într-un spectacol judiciar plin de umor teatral, finalizat printr-un verdict dramatic dublat de un temei juridic factual din legislația reală a României.

---

## 🛠️ Tech Stack

| Componentă | Tehnologie / Framework |
|---|---|
| **Backend API** | Python 3.11 / FastAPI |
| **Orchestrare Multi-Agent** | Python Custom Pipeline (Autonom / Interactiv Multi-turn) |
| **Modele LLM Inference** | Groq Cloud API (Llama 3.1 8B Instant / Llama 3 8B) |
| **Frontend UI** | React 19 / Vite / Tailwind CSS |
| **Automatizare Teste / Evals** | pytest / Custom LLM Evaluation Framework |
| **Pipeline CI/CD** | GitHub Actions |

---

## 📌 Corelarea cu Baremul de Notare MDS

| Componentă Barem | Punctaj | Locație în Repository / Dovada Implementării |
|---|---|---|
| **A. Implementare & Live Demo** | 7 pct | Aplicație complet funcțională Backend-Frontend. Integrare stabilă Groq API cu mecanisme de retry în `base_agent.py`. |
| **A. Minim 2 Agenți AI în funcționalitate** | 3 pct | Proiectul depășește cerința minimă, implementând **5 agenți AI specializați**: `InterrogatorAgent`, `ComplainantAgent`, `ProsecutorAgent`, `JudgeAgent`, `LegalResearchAgent`. [Vezi folderul de agenți](./src/agents/). |
| **A. Demo Offline (Screencast)** | — | 🎥 [Urmăriți Prezentarea Video pe YouTube](PUNE_LINKUL_TAU_DE_YOUTUBE_AICI) |
| **B1. User Stories & Backlog Creation** | 2 pct | [BACKLOG.md](./BACKLOG.md) — Conține 14 User Stories complete cu criterii de acceptanță clare, structurate pe 6 Epics tehnice. |
| **B2. Diagrame (Arhitectură & Workflow)** | 1 pct | [arhitectura.md](./arhitectura.md) — Diagramă de workflow și interacțiune asincronă multi-agent randată nativ în format Mermaid.js. |
| **B3. Source Control cu Git** | 1 pct | Lucru colaborativ pe branch-uri de feature, Pull Requests pentru integrare și minim 5 commit-uri per student (vezi istoricul de Git). |
| **B4. Teste Automate & Agent Evals** | 2 pct | Unit Tests în [src/agents/test_agents.py](./src/agents/test_agents.py) și un sistem complet de LLM Evals în [evals/run_evals.py](./evals/run_evals.py) cu generare automată de raport calitativ în [evals_report.md](./evals/evals_report.md). |
| **B5. Raportare Bug și Rezolvare cu PR** | 1 pct | Corectarea bug-ului logic din scriptul de evaluare legat de severitatea `CATASTROPHIC`. [Vezi Pull Request #1](https://github.com/mihneadrg/AI-Judge---MDS/pull/3) și [Issue #1](https://github.com/mihneadrg/AI-Judge---MDS/issues). |
| **B6. Pipeline CI/CD** | 1 pct | [.github/workflows/tests.yml](./.github/workflows/tests.yml) — Flux automatizat prin GitHub Actions care instalează dependențele și rulează suita de teste la fiecare Push sau Pull Request pe branch-ul `main`. |
| **B7. Raport utilizare tool-uri AI** | 2 pct | [raport_ai.md](./raport_ai.md) — Document exhaustiv ce detaliază modul în care Claude, Gemini și GitHub Copilot au asistat echipa în design, prompt engineering și codare. |

---

## 📂 Structura Proiectului

```text
siem-tool/
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline CI/CD automatizat pentru teste
├── backend/                   # 🐘 PHP / Symfony 8 (REST API + SSE via Mercure)
│   └── src/
│       ├── Controller/        # Endpoints API (Alert, Config, Event, Incident, Rule)
│       ├── Entity/            # Modele de date Doctrine ORM
│       ├── Repository/        # Repozitorii pentru operațiuni pe baza de date
│       └── Service/           # Logica de business (ex. EventPublisher pentru SSE)
├── frontend/                  # ⚛️ React / TypeScript UI
│   └── src/
│       └── tests/             # Teste automate (Vitest)
├── services/                  # 🐍 Microservicii autonome Python
│   ├── agents/                # Integrare LLM (Ollama) pentru decizii de securitate
│   │   └── tests/
│   │       └── test_agent_evals.py # Evaluări automate pentru modelele de limbaj
│   ├── capture/               # Packet sniffer cu Scapy și parsare de trafic
│   └── rules/                 # Motorul de detecție și trigger pentru alerte
├── docs/                      # Documentația tehnică a proiectului
│   ├── diagrams/              # Diagrame UML, secvență și arhitectură
│   └── SIEM_backlog.md        # Planificarea Agile (User stories)
└── docker-compose.yml         # 🐳 Orchestrare containere (Redis, DB, AI Agents)

---

## 🤖 Arhitectura Agenților AI

Sistemul utilizează un lanț de execuție specializat pentru a asigura atât valoarea de divertisment, cât și rigoarea tehnică:
1. **Interactive Mode:** Utilizatorul introduce plângerea -> `InterrogatorAgent` analizează contextul și adresează dinamic până la 3 întrebări pentru clarificare -> `ProsecutorAgent` compilează rechizitoriul și stabilește nivelul de severitate -> `JudgeAgent` emite sentința dramatică -> `LegalResearchAgent` ancorează cazul într-un articol real din Codul Penal sau Civil.
2. **Autonomous Watch Mode:** `ComplainantAgent` generează automat o speță absurdă și răspunde de la sine la întrebările puse de instanță, utilizatorul având rolul de spectator la întregul proces derulat în timp real.

---

## 🚀 Ghid de Instalare și Rulare Locală

### 1. Configurare Backend (Python)
Asigurați-vă că aveți un fișier `.env` în root-ul proiectului care conține cheia dumneavoastră de API:
```env
GROQ_API_KEY=cheia_ta_de_la_groq_console

Rulați următoarele comenzi în terminal pentru a configura mediul virtual și a porni serverul:

# Instalarea dependențelor direct din requirements
pip install -r requirements.txt

# Pornirea serverului FastAPI pe portul 8000
python -m uvicorn src.main:app --reload --port 8000

2. Configurare Frontend (React)
Într-o nouă fereastră de terminal, navigați în folderul proiectului și rulați:

# Instalarea pachetelor Node.js
npm install

# Pornirea serverului de dezvoltare Vite
npm run dev

3. Rularea Testelor și Evaluărilor LLM
Pentru a verifica conformitatea structurală a agenților și a rula scripturile de calitate:

# Rularea testelor unitare automate (pytest)
pytest src/agents/ -v

# Rularea pipeline-ului de evaluare calitativă a răspunsurilor LLM
python evals/run_evals.py