from .base_agent import BaseAgent

JUDGE_SYSTEM_PROMPT = """You are ONORABILA JUDECĂTOARE DRAMATICUS MAXIMUS III, \
the most theatrical judge in the Dramatic AI Court of Justice.

CRITICAL: Respond with ONLY a valid JSON object. No text before or after. No markdown.
IMPORTANT: Write ALL text values in Romanian language.

The JSON must have exactly these 8 fields:
{
  "case_title": "titlu dramatic care face referire la evenimentele REALE",
  "charges": "reafirmă acuzațiile REALE în limbaj juridic grandios",
  "evidence_presented": "rezumă dramatic dovezile REALE — fii specific",
  "legal_precedent": "inventează un precedent fictiv pentru ACEST caz specific (nume fals + an fals)",
  "verdict": "VINOVAT or NEVINOVAT",
  "sentence": "pedeapsă creativă care se potrivește cu crima REALĂ",
  "legal_reasoning": "2-3 propoziții dramatice care fac referire la faptele REALE",
  "courts_final_words": "închidere memorabilă care face referire la crima SPECIFICĂ"
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
            "case_title": parsed.get("case_title", "Cazul Adus în Fața Curții"),
            "charges": parsed.get("charges", "Acuzații conform rechizitoriului"),
            "evidence_presented": parsed.get("evidence_presented", "Dovezi prezentate instanței"),
            "legal_precedent": parsed.get("legal_precedent", "Popescu vs. Circumstanță (1899)"),
            "verdict": self._normalize_verdict(parsed.get("verdict", "VINOVAT")),
            "sentence": parsed.get("sentence", "Reflectați asupra faptelor dumneavoastră."),
            "legal_reasoning": parsed.get("legal_reasoning", "Curtea consideră conduita inacceptabilă."),
            "courts_final_words": parsed.get("courts_final_words", "Curtea se ridică!"),
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
        if any(w in t for w in ("NEVINOVAT", "NOT GUILTY", "INNOCENT", "ACHITAT")):
            return "NEVINOVAT"
        return "VINOVAT"

    def _fallback_response(self, reason: str, raw_response: str = "") -> dict:
        partial = self._safe_parse_json(raw_response) if raw_response else {}
        return {
            "case_title": partial.get("case_title", "Cazul Adus în Fața Curții"),
            "charges": partial.get("charges", "Acuzații conform rechizitoriului"),
            "evidence_presented": partial.get("evidence_presented", "Dovezi prezentate instanței"),
            "legal_precedent": partial.get("legal_precedent", "Popescu vs. Circumstanță (1899)"),
            "verdict": self._normalize_verdict(partial.get("verdict", "VINOVAT")),
            "sentence": partial.get("sentence", "Reflectați asupra faptelor dumneavoastră timp de două săptămâni."),
            "legal_reasoning": partial.get("legal_reasoning", "Curtea consideră conduita inacceptabilă."),
            "courts_final_words": partial.get("courts_final_words", "Curtea se ridică!"),
            "error": reason,
            "raw_response": raw_response,
            "agent": "JudgeAgent",
            "model_used": self.model,
        }