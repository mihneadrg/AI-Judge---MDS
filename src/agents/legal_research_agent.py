"""
Legal Research Agent - Agentul de Documentare Juridică.

Rulează DUPĂ ce JudgeAgent a pronunțat verdictul. Primește verdictul și
contextul cazului și caută, printr-un apel LLM, articolul de lege REAL din
legislația română care fundamentează verdictul (Codul Penal, Codul Civil,
Codul Contravențional etc.).

Spre deosebire de ceilalți agenți (care sunt deliberat teatrali și inventează
precedente fictive), acest agent trebuie să fie FACTUAL și sobru: articolele
de lege returnate trebuie să existe cu adevărat. Rezultatul este pur informativ
și nu constituie consultanță juridică.
"""

from .base_agent import BaseAgent


LEGAL_RESEARCH_SYSTEM_PROMPT = """You are CONSILIERUL JURIDIC AL CURȚII, a sober legal \
research assistant for the Dramatic AI Court of Justice.

Unlike the theatrical judge, you are FACTUAL and precise. Your job: given a case and \
its verdict, identify the REAL article of Romanian law that best applies to the facts.

CRITICAL: Respond with ONLY a valid JSON object. No text before or after. No markdown.
IMPORTANT: Write ALL text values in Romanian language.

The JSON must have exactly these 6 fields:
{
  "law_code": "codul de lege REAL din România (ex: Codul Penal, Codul Civil, OUG 195/2002 privind circulația, Codul Contravențional)",
  "article_number": "numărul articolului REAL (ex: Art. 228)",
  "article_title": "denumirea/marginalul articolului (ex: Furtul)",
  "article_text": "un rezumat fidel al conținutului articolului, în 1-2 propoziții",
  "relevance": "1-2 propoziții care explică de ce acest articol se aplică faptelor SPECIFICE din caz",
  "disclaimer": "Informație juridică orientativă, nu constituie consultanță juridică."
}

Rules:
- The article MUST be a real provision of Romanian law — never invent article numbers.
- If no criminal provision fits, you may cite civil or contravention law.
- Map the facts to the closest real offence (ex: furt → Art. 228 Cod Penal; \
tulburarea liniștii → Legea 61/1991; vătămare → Art. 193 Cod Penal).
- Keep "article_text" faithful to the actual legal content, not dramatic.
- Output ONLY the JSON object. Nothing else.
"""


class LegalResearchAgent(BaseAgent):
    """
    Agentul de Documentare Juridică — rulează după JudgeAgent.

    Caută articolul de lege real care fundamentează verdictul.

    Exemplu de utilizare:
        agent = LegalResearchAgent(model="llama3")
        result = agent.run({"verdict": verdict_dict, "prosecution": prosecution_dict})
        print(result["article_number"], result["article_title"])
    """

    def __init__(self, model: str = "llama3", temperature: float = 0.2):
        # Temperatură MICĂ — vrem acuratețe juridică, nu creativitate.
        super().__init__(model=model, temperature=temperature)

    def run(self, input_data) -> dict:
        """
        Identifică articolul de lege aplicabil pe baza verdictului și a cazului.

        Args:
            input_data: fie un dict {"verdict": ..., "prosecution": ...},
                        fie un string cu descrierea situației.

        Returns:
            Dict cu articolul de lege:
            {
                "law_code": str,
                "article_number": str,
                "article_title": str,
                "article_text": str,
                "relevance": str,
                "disclaimer": str,
                "raw_response": str,
                "agent": "LegalResearchAgent",
                "model_used": str
            }
        """
        if isinstance(input_data, dict):
            user_message = self._format_case_message(input_data)
        elif isinstance(input_data, str) and input_data.strip():
            user_message = (
                f'CASE FACTS: "{input_data.strip()}"\n'
                "Identify the applicable Romanian law article. JSON only."
            )
        else:
            return self._fallback_response("Input invalid.")

        raw_response = self._call_ollama(LEGAL_RESEARCH_SYSTEM_PROMPT, user_message)
        parsed = self._safe_parse_json(raw_response)

        if parsed is None:
            return self._fallback_response("JSON invalid.", raw_response=raw_response)

        return {
            "law_code": parsed.get("law_code", "Codul Penal al României"),
            "article_number": parsed.get("article_number", "Art. necunoscut"),
            "article_title": parsed.get("article_title", "Dispoziție legală aplicabilă"),
            "article_text": parsed.get(
                "article_text", "Conținutul articolului nu a putut fi determinat."
            ),
            "relevance": parsed.get(
                "relevance", "Articolul se raportează la faptele descrise în caz."
            ),
            "disclaimer": parsed.get(
                "disclaimer",
                "Informație juridică orientativă, nu constituie consultanță juridică.",
            ),
            "raw_response": raw_response,
            "agent": "LegalResearchAgent",
            "model_used": self.model,
        }

    def _format_case_message(self, data: dict) -> str:
        """Construiește mesajul pentru LLM din verdict + dosarul de acuzare."""
        verdict = data.get("verdict", {}) or {}
        prosecution = data.get("prosecution", {}) or {}

        charges = prosecution.get("formal_charges", [])
        charges_text = "\n".join(f"  - {c}" for c in charges) if charges else "  (n/a)"

        return f"""CASE FILE:
ORIGINAL COMPLAINT: "{prosecution.get('original_input', '')}"
CASE TYPE: {prosecution.get('case_type', 'Unknown')}
FORMAL CHARGES:
{charges_text}
VERDICT: {verdict.get('verdict', 'N/A')}
CHARGES (judge): {verdict.get('charges', '')}
LEGAL REASONING: {verdict.get('legal_reasoning', '')}

Identify the single most applicable REAL Romanian law article for these facts. JSON only."""

    def _fallback_response(self, reason: str, raw_response: str = "") -> dict:
        """Răspuns de rezervă când modelul eșuează sau input-ul e invalid."""
        partial = self._safe_parse_json(raw_response) or {}
        return {
            "law_code": partial.get("law_code", "Codul Penal al României"),
            "article_number": partial.get("article_number", "Art. nedeterminat"),
            "article_title": partial.get("article_title", "Dispoziție legală aplicabilă"),
            "article_text": partial.get(
                "article_text",
                "Articolul de lege nu a putut fi identificat pentru acest caz.",
            ),
            "relevance": partial.get(
                "relevance", "Documentarea juridică nu a putut fi finalizată."
            ),
            "disclaimer": partial.get(
                "disclaimer",
                "Informație juridică orientativă, nu constituie consultanță juridică.",
            ),
            "error": reason,
            "raw_response": raw_response,
            "agent": "LegalResearchAgent",
            "model_used": self.model,
        }
