# Arhitectura Sistemului: The Dramatic AI Judge

## Workflow Agenți AI

```mermaid
graph TD
    A[Utilizator] -->|Introduce Situația| B(React Frontend)
    B -->|POST /api/v1/start| C{FastAPI Backend}
    
    C --> D[Court Pipeline Orchestrator]
    
    D -->|1. Dacă e nevoie de info| E[InterrogatorAgent]
    E -->|Întrebări| A
    A -->|Răspunsuri| D
    
    D -->|2. Context Complet| F[ProsecutorAgent]
    F -->|Construiește Acuzarea| G[JudgeAgent]
    G -->|Pronunță Verdictul| H[LegalResearchAgent]
    
    H -->|Caută Legea Reală| I[Rezultat Final JSON]
    I --> B