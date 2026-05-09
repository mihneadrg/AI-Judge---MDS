"""
Prosecutor Agent - Agentul Procuror.

Primul agent din pipeline. Primește situația brută de la utilizator
și construiește dosarul de acuzare: tipul cazului, acuzațiile formale
și probele identificate. Output-ul structurat merge mai departe la Judge Agent.
"""

from .base_agent import BaseAgent


PROSECUTOR_SYSTEM_PROMPT = PROSECUTOR_SYSTEM_PROMPT = """You are PROSECUTOR MAXIMUS, the most dramatic and theatrical \
prosecutor in the history of the Dramatic AI Court of Justice.

CRITICAL: Respond with ONLY a valid JSON object. No text before or after. No markdown.

The JSON must have exactly these fields:
{
  "case_type": "short category based on the ACTUAL situation",
  "severity_level": "one of: PETTY | MODERATE | SEVERE | CATASTROPHIC",
  "formal_charges": ["charge directly about what happened", "second specific charge", "third related charge"],
  "evidence_list": ["specific fact from the situation", "another specific detail", "logical inference"],
  "prosecution_summary": "one dramatic sentence that mentions the ACTUAL events",
  "recommended_sentence_hint": "a punishment hint that fits the SPECIFIC crime"
}

Rules:
- Every field MUST reference the ACTUAL situation — no generic placeholders
- Charges must be about what ACTUALLY happened
- Evidence must come from ACTUAL details in the complaint
- Use Latin phrases for drama (in flagrante delicto, mens rea, etc.)
- Output ONLY the JSON object. Nothing else.
"""


class ProsecutorAgent(BaseAgent):
    """
    Agentul Procuror — primul agent din pipeline.

    Analizează situația utilizatorului și construiește dosarul de acuzare
    cu acuzații dramatice, probe și o clasificare a cazului.

    Exemplu de utilizare:
        agent = ProsecutorAgent(model="llama3")
        result = agent.run("Vecinul meu cântă la chitară la 3 dimineața")
        print(result["formal_charges"])
    """

    def __init__(self, model: str = "llama3", temperature: float = 0.8):
        # Temperatura mai mare = mai dramatic și creativ
        super().__init__(model=model, temperature=temperature)

    def run(self, input_data: str) -> dict:
        """
        Procesează situația utilizatorului și construiește dosarul de acuzare.

        Args:
            input_data: Descrierea situației de la utilizator (text liber)

        Returns:
            Dict cu dosarul de acuzare:
            {
                "case_type": str,
                "severity_level": str,
                "formal_charges": list[str],
                "evidence_list": list[str],
                "prosecution_summary": str,
                "recommended_sentence_hint": str,
                "raw_response": str  # răspunsul brut al modelului (pentru debugging)
            }
        """
        if not input_data or not input_data.strip():
            return self._fallback_response("Input-ul este gol.")

        user_message = f"""CITIZEN'S COMPLAINT:
\"{input_data.strip()}\"

Analyze this situation and build the prosecution case. Respond with JSON only."""

        raw_response = self._call_ollama(PROSECUTOR_SYSTEM_PROMPT, user_message)
        print("=== PROSECUTOR RAW ===")
        print(repr(raw_response[:500]))
        print("======================")
        parsed = self._safe_parse_json(raw_response)

        if parsed is None:
            # Dacă modelul nu a generat JSON valid, returnăm un fallback
            return self._fallback_response(
                "Modelul nu a generat un răspuns JSON valid.",
                raw_response=raw_response,
                original_input=input_data,
            )

        # Validăm că avem câmpurile necesare și adăugăm fallback-uri
        result = {
            "case_type": parsed.get("case_type", "Unclassified Misconduct"),
            "severity_level": parsed.get("severity_level", "MODERATE"),
            "formal_charges": parsed.get("formal_charges", ["Conduct Unbecoming a Citizen"]),
            "evidence_list": parsed.get("evidence_list", ["Circumstantial evidence"]),
            "prosecution_summary": parsed.get("prosecution_summary", "The facts speak for themselves."),
            "recommended_sentence_hint": parsed.get("recommended_sentence_hint", "Justice shall prevail."),
            "raw_response": raw_response,
            "original_input": input_data,
            "agent": "ProsecutorAgent",
            "model_used": self.model,
        }

        return result

    def _fallback_response(self, reason: str, raw_response: str = "", original_input: str = "") -> dict:
        """Răspuns de rezervă când modelul eșuează."""
        return {
            "case_type": "Unclassified Misconduct",
            "severity_level": "MODERATE",
            "formal_charges": [
                "Conduct Unbecoming a Citizen",
                "Disturbance of the Social Order",
                "Failure to Maintain Acceptable Standards",
            ],
            "evidence_list": [
                "The complainant's testimony",
                "General circumstantial evidence",
                "The defendant's suspicious demeanor",
            ],
            "prosecution_summary": "The accused stands before this court charged with grievous misconduct.",
            "recommended_sentence_hint": "The court shall determine an appropriate punishment.",
            "error": reason,
            "raw_response": raw_response,
            "original_input": original_input,
            "agent": "ProsecutorAgent",
            "model_used": self.model,
        }
