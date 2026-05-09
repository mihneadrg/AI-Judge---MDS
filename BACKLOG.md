# 📋 Product Backlog - The Dramatic AI Judge

Acest document conține Epic-urile și User Story-urile necesare pentru dezvoltarea aplicației. Prioritizarea este făcută de sus în jos (Epic 1 fiind cel mai important).

## 🚀 Epic 1: Arhitectură, Setup și Infrastructură Bază
Acest epic se concentrează pe fundația tehnică a proiectului, pregătind mediul de dezvoltare în Python și stabilind arhitectura.

**[US-1.1] Configurare Mediu de Dezvoltare**
* **User Story:** Ca dezvoltator, vreau să configurez structura de directoare și mediul virtual Python (compatibil cu mediul de lucru pe Windows), astfel încât să pot gestiona dependențele izolat și eficient.
* **Criterii de Acceptanță:**
  * Există un fișier `requirements.txt` sau `pyproject.toml`.
  * Fișierul `.gitignore` exclude fișierele specifice sistemului de operare și directoarele `.env` sau `venv/`.
  * Structura proiectului separă clar logica sursă (`src/`) de teste (`tests/`).

**[US-1.2] Setup Endpoint-uri API (Backend)**
* **User Story:** Ca dezvoltator, vreau să inițializez un server de bază (ex: FastAPI/Flask) cu un endpoint de `POST`, astfel încât interfața să poată trimite datele către logica internă.
* **Criterii de Acceptanță:**
  * Serverul pornește fără erori pe `localhost`.
  * Un request de test către endpoint returnează codul HTTP 200 OK.

---

## 🧠 Epic 2: Core AI Logic & Prompt Engineering
Aici este implementată inima aplicației: comunicarea cu modelul de limbaj și aplicarea "persona-ului" de judecător dramatic.

**[US-2.1] Integrare Client LLM**
* **User Story:** Ca sistem, vreau să mă pot autentifica și conecta la API-ul LLM-ului în mod securizat, astfel încât să pot trimite prompt-uri și primi răspunsuri.
* **Criterii de Acceptanță:**
  * Cheia API este citită dintr-un fișier `.env` (niciodată hardcodată).
  * Există un mecanism de try-catch pentru a gestiona erorile de rețea sau de autentificare cu API-ul.

**[US-2.2] Procesarea Situației prin "The Judge Persona"**
* **User Story:** Ca utilizator, vreau ca situația mea cotidiană să fie analizată printr-un prompt teatral specific, astfel încât rezultatul să fie o judecată completă și amuzantă.
* **Criterii de Acceptanță:**
  * Sistemul injectează input-ul utilizatorului în *system prompt-ul* predefinit ("Act as a dramatic judge...").
  * Output-ul de la LLM conține obligatoriu cele 8 câmpuri cerute: Case Title, Charges, Evidence Presented, Legal Precedent, VERDICT, Sentence, Legal Reasoning, Court's Final Words.

**[US-2.3] Parsarea și Structurarea Output-ului**
* **User Story:** Ca sistem, vreau să extrag exact secțiunile din răspunsul LLM-ului într-un format structurat (ex: dicționar/JSON), astfel încât backend-ul să poată trimite date clare către frontend.
* **Criterii de Acceptanță:**
  * Se folosește un parser cu expresii regulate (Regex) sau un *structured output format* nativ al LLM-ului pentru a separa câmpurile.
  * Dacă LLM-ul omite o secțiune, sistemul returnează un mesaj de eroare grațios sau o valoare default ("N/A").

---

## 🖥️ Epic 3: Interacțiunea cu Utilizatorul (Interfață)
Acest epic definește modul în care utilizatorul final introduce datele și citește rezultatul.

**[US-3.1] Formularul de Reclamație**
* **User Story:** Ca utilizator, vreau să am la dispoziție un câmp de text simplu unde să descriu situația, astfel încât să pot trimite cazul meu instanței AI.
* **Criterii de Acceptanță:**
  * Input-ul acceptă texte de până la 1000 de caractere.
  * Nu se pot trimite cereri goale (validare pe frontend/backend).

**[US-3.2] Afișarea Verdictului Teatral**
* **User Story:** Ca utilizator, vreau să văd răspunsul împărțit clar pe categorii cu un design ce amintește de un document legal, astfel încât să fie ușor de citit și imersiv.
* **Criterii de Acceptanță:**
  * Fiecare dintre cele 8 câmpuri (Case Title, Charges etc.) este afișat distinct (ex: cu bold sau ca titlu de secțiune).
  * Verdictul final și Sentința sunt evidențiate vizual.

---

## 🛡️ Epic 4: Quality Assurance & Error Handling
Asigurarea robusteței aplicației.

**[US-4.1] Validarea Textului de Intrare**
* **User Story:** Ca dezvoltator, vreau să implementez un filtru de bază pe datele de intrare, astfel încât sistemul să nu proceseze scripturi malițioase sau texte invalide.
* **Criterii de Acceptanță:**
  * Input-ul este sanitizat înainte de a fi trimis către LLM.

**[US-4.2] Teste Unitare pentru Parser-ul de Output**
* **User Story:** Ca dezvoltator, vreau să scriu teste automate pentru modulul care sparge textul LLM-ului în categorii, astfel încât să garantez că logica de afișare nu va crăpa la răspunsuri neașteptate.
* **Criterii de Acceptanță:**
  * Există cel puțin un test case pentru un răspuns ideal, formatat perfect de LLM.
  * Există cel puțin un test case pentru un răspuns parțial sau greșit formatat de LLM.