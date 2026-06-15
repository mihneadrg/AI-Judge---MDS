# Raport de Utilizare a Tool-urilor AI în Dezvoltare

Acest proiect a fost dezvoltat folosind o abordare "AI-First", integrând asistenți bazați pe LLM-uri în toate etapele ciclului de dezvoltare software (SDLC).

## 1. Faza de Planificare și Arhitectură
* **Generare Backlog:** Am folosit Gemini pentru a transforma ideea de bază într-o structură agilă. AI-ul ne-a generat cele 6 Epics și ne-a ajutat la formularea celor 14 User Stories din `BACKLOG.md`.
* **Proiectarea Agenților:** Arhitectura multi-agent a fost rafinată printr-un brainstorming iterativ cu Claude 3.5 Sonnet, pentru a asigura separarea clară a responsabilităților între procuror, judecător și interogator.

## 2. Faza de Implementare (Cod)
* **Backend și Frontend:** Am utilizat GitHub Copilot direct în IDE pentru a scrie rapid boilerplate-ul claselor de agenți, logica de parsare a JSON-ului și componentele React. Copilot ne-a ajutat imens la autocompletarea structurilor repetitive.
* **Prompt Engineering:** Prompturile de sistem pentru fiecare personaj au fost generate și ajustate cu ajutorul Claude și Gemini pentru a asigura formatul strict JSON și tonul dramatic în limba română.

## 3. Faza de Testare și QA
* **Generare Test Cases:** Fișierul `evals/test_cases.json` conține scenarii de plângeri cotidiene generate complet cu Gemini, acoperind diverse tipuri de conflicte.
* **Scripturi de Evaluare:** Am creat pipeline-ul din `run_evals.py` asistat de Copilot, care măsoară calitatea răspunsurilor și robustețea la halucinații.