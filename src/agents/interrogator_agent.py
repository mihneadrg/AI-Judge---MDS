"""
Interrogator Agent - Agentul Interogator.

Al treilea agent din pipeline (rulează primul).
Primește situația inițială și decide dacă are nevoie de mai multe informații.
Pune maxim 3 întrebări, una câte una, într-un stil dramatic de tribunal.
"""

from .base_agent import BaseAgent


INTERROGATOR_SYSTEM_PROMPT = """You are INCHIZITORUL SEVERUS of the AI Court.

CRITICAL: Respond with ONLY a valid JSON object. No text before or after. No markdown.
IMPORTANT: Write ALL values in Romanian. Keep strings UNDER 20 WORDS each.

{
  "needs_more_info": true or false,
  "question": "a short specific question in Romanian (max 20 words) — REQUIRED if needs_more_info is true, empty string if false",
  "reason": "reason in max 15 words"
}

Rules:
- If needs_more_info is true, question MUST be a non-empty Romanian sentence.
- If needs_more_info is false, question must be an empty string "".
- Ask max 1 question total across the whole interrogation.
- Output ONLY the JSON. Nothing else.
"""


class InterrogatorAgent(BaseAgent):
    """
    Agentul Interogator — pune întrebări dramatice pentru a clarifica cazul.

    Rulează în buclă până când are suficiente informații (max 3 întrebări).
    Output-ul său (contextul complet) merge la ProsecutorAgent.

    Exemplu de utilizare:
        agent = InterrogatorAgent(model="llama3")
        result = agent.run({
            "situation": "Vecinul cântă noaptea",
            "qa_history": []
        })
        if result["needs_more_info"]:
            print(result["question"])  # "De câte ori pe săptămână se întâmplă acest lucru?"
    """

    def __init__(self, model: str = "llama3", temperature: float = 0.7):
        super().__init__(model=model, temperature=temperature)

    def run(self, input_data: dict) -> dict:
        """
        Decide dacă e nevoie de mai multe informații și formulează întrebarea.

        Args:
            input_data: dict cu:
                - "situation": str — descrierea inițială
                - "qa_history": list — lista de (întrebare, răspuns) anterioare
                - "questions_asked": int — câte întrebări s-au pus deja

        Returns:
            {
                "needs_more_info": bool,
                "question": str,
                "reason": str,
                "agent": str
            }
        """
        situation = input_data.get("situation", "")
        qa_history = input_data.get("qa_history", [])
        questions_asked = input_data.get("questions_asked", 0)

        # Dacă am pus deja 3 întrebări, oprim
        if questions_asked >= 3:
            return {
                "needs_more_info": False,
                "question": "",
                "reason": "Curtea are suficiente informații pentru a pronunța verdictul.",
                "agent": "InterrogatorAgent",
            }

        user_message = self._build_message(situation, qa_history, questions_asked)
        raw_response = self._call_ollama(INTERROGATOR_SYSTEM_PROMPT, user_message)
        parsed = self._safe_parse_json(raw_response)

        if parsed is None:
            return {
                "needs_more_info": False,
                "question": "",
                "reason": "Curtea procedează cu informațiile disponibile.",
                "agent": "InterrogatorAgent",
            }

        return {
            "needs_more_info": bool(parsed.get("needs_more_info", False)),
            "question": parsed.get("question", ""),
            "reason": parsed.get("reason", ""),
            "agent": "InterrogatorAgent",
        }

    def _build_message(self, situation: str, qa_history: list, questions_asked: int) -> str:
        """Construiește mesajul pentru model cu tot contextul conversației."""
        history_text = ""
        if qa_history:
            history_text = "\n\nPREVIOUS QUESTIONS AND ANSWERS:\n"
            for i, (q, a) in enumerate(qa_history, 1):
                history_text += f"Q{i}: {q}\nA{i}: {a}\n"

        return f"""INITIAL SITUATION: "{situation}"
{history_text}
QUESTIONS ASKED SO FAR: {questions_asked}/3

Do you need more information to build a proper dramatic case? 
Respond with JSON only."""
