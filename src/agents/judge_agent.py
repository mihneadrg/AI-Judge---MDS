from .base_agent import BaseAgent

JUDGE_SYSTEM_PROMPT = """You are THE HONOURABLE JUDGE DRAMATICUS MAXIMUS III, \
the most theatrical judge in the Dramatic AI Court of Justice.

CRITICAL: Respond with ONLY a valid JSON object. No text before or after. No markdown.

The JSON must have exactly these 8 fields:
{
  "case_title": "dramatic title referencing the ACTUAL events",
  "charges": "restate ACTUAL charges in grandiose legal language",
  "evidence_presented": "dramatically summarize the ACTUAL evidence — be specific",
  "legal_precedent": "invent a fictional precedent for THIS specific case (fake name + fake year)",
  "verdict": "GUILTY or NOT GUILTY",
  "sentence": "creative punishment that fits the ACTUAL crime",
  "legal_reasoning": "2-3 dramatic sentences referencing the ACTUAL facts",
  "courts_final_words": "memorable closing referencing the SPECIFIC crime"
}

Rules:
- Every field MUST reference the ACTUAL case — never generic
- Sentence must fit the crime: pizza theft = food punishment; noise = silence punishment
- Be EXTREMELY theatrical
- Output ONLY the JSON object. Nothing else.
"""


class JudgeAgent(BaseAgent):

    def __init__(self, model: str = "llama3", temperature: float = 0.9):
        super().__init__(model=model, temperature=temperature)

    def run(self, input_data) -> dict:
        if isinstance(input_data, dict):
            user_message = self._format_prosecution_message(input_data)
        elif isinstance(input_data, str):
            user_message = f'SITUATION: "{input_data}"\nDeliver verdict. JSON only.'
        else:
            return self._fallback_response("Input invalid.")

        raw_response = self._call_ollama(JUDGE_SYSTEM_PROMPT, user_message)
        print("=== JUDGE RAW ===")
        print(repr(raw_response[:300]))
        print("=================")
        parsed = self._safe_parse_json(raw_response)

        if parsed is None:
            return self._fallback_response("JSON invalid.", raw_response=raw_response)

        return {
            "case_title": parsed.get("case_title", "The Case Before This Court"),
            "charges": parsed.get("charges", "Charges as presented"),
            "evidence_presented": parsed.get("evidence_presented", "Evidence as submitted"),
            "legal_precedent": parsed.get("legal_precedent", "Rex v. Circumstance (1899)"),
            "verdict": self._normalize_verdict(parsed.get("verdict", "GUILTY")),
            "sentence": parsed.get("sentence", "Reflect upon your actions."),
            "legal_reasoning": parsed.get("legal_reasoning", "The court finds the conduct inexcusable."),
            "courts_final_words": parsed.get("courts_final_words", "Court adjourned!"),
            "raw_response": raw_response,
            "agent": "JudgeAgent",
            "model_used": self.model,
        }

    def _format_prosecution_message(self, prosecution: dict) -> str:
        charges = "\n".join(f"  {i+1}. {c}" for i, c in enumerate(prosecution.get("formal_charges", [])))
        evidence = "\n".join(f"  - {e}" for e in prosecution.get("evidence_list", []))
        return f"""PROSECUTION CASE:
CASE TYPE: {prosecution.get('case_type', 'Unknown')}
SEVERITY: {prosecution.get('severity_level', 'MODERATE')}
ORIGINAL COMPLAINT: "{prosecution.get('original_input', '')}"
CHARGES:\n{charges}
EVIDENCE:\n{evidence}
SUMMARY: {prosecution.get('prosecution_summary', '')}
Deliver your verdict. JSON only."""

    def _normalize_verdict(self, text: str) -> str:
        t = text.upper()
        if "NOT GUILTY" in t or "INNOCENT" in t:
            return "NOT GUILTY"
        return "GUILTY"

    def _fallback_response(self, reason: str, raw_response: str = "") -> dict:
        partial = self._safe_parse_json(raw_response) if raw_response else {}
        return {
            "case_title": partial.get("case_title", "The Case Before This Court"),
            "charges": partial.get("charges", "Charges as presented by the prosecution"),
            "evidence_presented": partial.get("evidence_presented", "Evidence as submitted"),
            "legal_precedent": partial.get("legal_precedent", "Rex v. Circumstance (1899)"),
            "verdict": self._normalize_verdict(partial.get("verdict", "GUILTY")),
            "sentence": partial.get("sentence", "Reflect upon your actions for one fortnight."),
            "legal_reasoning": partial.get("legal_reasoning", "The court finds the conduct inexcusable."),
            "courts_final_words": partial.get("courts_final_words", "Court adjourned!"),
            "error": reason,
            "raw_response": raw_response,
            "agent": "JudgeAgent",
            "model_used": self.model,
        }