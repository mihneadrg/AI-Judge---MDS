"""
Agent Pipeline - Orchestrarea celor trei agenți cu conversație multi-turn.

Fluxul complet:
    1. User descrie situația
    2. InterrogatorAgent pune întrebări (max 3), una câte una
    3. Când are suficiente info → ProsecutorAgent construiește dosarul
    4. JudgeAgent pronunță verdictul final
"""

import time
import uuid
from .prosecutor_agent import ProsecutorAgent
from .judge_agent import JudgeAgent
from .interrogator_agent import InterrogatorAgent
from .complainant_agent import ComplainantAgent


# Stochează sesiunile active în memorie
# { session_id: { situation, qa_history, questions_asked, state } }
_sessions: dict = {}


class CourtPipeline:
    """
    Orchestratorul pipeline-ului de agenți cu suport multi-turn.

    Stările unei sesiuni:
        "interrogating" — InterrogatorAgent pune întrebări
        "judging"       — se procesează verdictul (în curs)
        "done"          — verdictul a fost pronunțat
    """

    def __init__(self, model: str = "llama3"):
        self.model = model
        self.prosecutor = ProsecutorAgent(model=model, temperature=0.8)
        self.judge_agent = JudgeAgent(model=model, temperature=0.9)
        self.interrogator = InterrogatorAgent(model=model, temperature=0.7)

    # ── API public ────────────────────────────────────────────────────────────

    def start_case(self, situation: str) -> dict:
        """
        Începe un caz nou. Returnează fie prima întrebare, fie direct verdictul
        dacă situația e suficient de detaliată.

        Returns:
            {
                "session_id": str,
                "state": "question" | "verdict",
                "question": str | None,
                "verdict": dict | None,
                "questions_asked": int,
                "error": str | None
            }
        """
        session_id = str(uuid.uuid4())
        _sessions[session_id] = {
            "situation": situation,
            "qa_history": [],
            "questions_asked": 0,
            "state": "interrogating",
            "last_question": None,
        }

        return self._next_step(session_id)

    def answer_question(self, session_id: str, answer: str) -> dict:
        """
        Primește răspunsul utilizatorului la întrebarea curentă.
        Continuă cu următoarea întrebare sau trece la verdict.
        """
        if session_id not in _sessions:
            return {
                "session_id": session_id,
                "state": "error",
                "question": None,
                "verdict": None,
                "questions_asked": 0,
                "error": "Sesiunea nu există sau a expirat.",
            }

        session = _sessions[session_id]

        # Salvăm răspunsul la ultima întrebare
        if session.get("last_question"):
            session["qa_history"].append((session["last_question"], answer))
            session["questions_asked"] += 1

        return self._next_step(session_id)

    def judge(self, situation: str) -> dict:
        """Metodă simplă fără multi-turn — pentru compatibilitate."""
        start_time = time.time()
        if not situation or not situation.strip():
            return {"prosecution": {}, "final_verdict": {}, "model_used": self.model,
                    "processing_time_seconds": 0.0, "success": False,
                    "error": "Situația nu poate fi goală."}
        try:
            prosecution = self.prosecutor.run(situation)
            verdict = self.judge_agent.run(prosecution)
        except Exception as e:
            return self._error_response(str(e), start_time)

        return {"prosecution": prosecution, "final_verdict": verdict,
                "model_used": self.model,
                "processing_time_seconds": round(time.time() - start_time, 2),
                "success": True, "error": None}

    # ── Logică internă ────────────────────────────────────────────────────────

    def _next_step(self, session_id: str) -> dict:
        """Decide dacă punem o altă întrebare sau mergem la verdict."""
        session = _sessions[session_id]

        interrogation_result = self.interrogator.run({
            "situation": session["situation"],
            "qa_history": session["qa_history"],
            "questions_asked": session["questions_asked"],
        })

        if interrogation_result["needs_more_info"] and session["questions_asked"] < 3:
            question = interrogation_result["question"]
            session["last_question"] = question

            return {
                "session_id": session_id,
                "state": "question",
                "question": question,
                "verdict": None,
                "questions_asked": session["questions_asked"],
                "error": None,
            }
        else:
            return self._produce_verdict(session_id)

    def _produce_verdict(self, session_id: str) -> dict:
        """Rulează ProsecutorAgent + JudgeAgent cu tot contextul adunat."""
        session = _sessions[session_id]

        full_context = session["situation"]
        if session["qa_history"]:
            full_context += "\n\nAdditional context from court interrogation:"
            for q, a in session["qa_history"]:
                full_context += f"\n- {q}\n  Answer: {a}"

        start_time = time.time()
        try:
            prosecution = self.prosecutor.run(full_context)
            verdict = self.judge_agent.run(prosecution)
        except Exception as e:
            return {
                "session_id": session_id,
                "state": "error",
                "question": None,
                "verdict": None,
                "questions_asked": session["questions_asked"],
                "error": str(e),
            }

        _sessions.pop(session_id, None)

        return {
            "session_id": session_id,
            "state": "verdict",
            "question": None,
            "verdict": {
                "prosecution": prosecution,
                "final_verdict": verdict,
                "processing_time_seconds": round(time.time() - start_time, 2),
            },
            "questions_asked": session["questions_asked"],
            "error": None,
        }

    def run_autonomous_trial(self) -> dict:
        """
        Rulează un proces complet automat — fără input uman.

        ComplainantAgent generează situația și răspunde la întrebări.
        Returnează transcript complet cu toate etapele.

        Returns:
            {
                "complainant_name": str,
                "situation": str,
                "interrogation": [{ "question": str, "answer": str }, ...],
                "prosecution": dict,
                "final_verdict": dict,
                "processing_time_seconds": float,
            }
        """
        complainant = ComplainantAgent(model=self.model, temperature=0.9)
        start_time = time.time()

        # Pasul 1: Reclamantul generează o situație
        situation_data = complainant.generate_situation()
        situation = situation_data["situation"]
        complainant_name = situation_data["complainant_name"]

        # Pasul 2: Interogatoriu automat
        qa_history = []
        questions_asked = 0
        interrogation = []

        while questions_asked < 3:
            interrogation_result = self.interrogator.run({
                "situation": situation,
                "qa_history": qa_history,
                "questions_asked": questions_asked,
            })

            if not interrogation_result.get("needs_more_info"):
                break

            question = interrogation_result["question"]
            answer_data = complainant.answer_question(
                situation=situation,
                complainant_name=complainant_name,
                question=question,
                qa_history=qa_history,
            )
            answer = answer_data["answer"]

            qa_history.append((question, answer))
            interrogation.append({"question": question, "answer": answer})
            questions_asked += 1

        # Pasul 3: Construim contextul complet și pronunțăm verdictul
        full_context = situation
        if qa_history:
            full_context += "\n\nAdditional context from court interrogation:"
            for q, a in qa_history:
                full_context += f"\n- {q}\n  Answer: {a}"

        prosecution = self.prosecutor.run(full_context)
        verdict = self.judge_agent.run(prosecution)

        return {
            "complainant_name": complainant_name,
            "situation": situation,
            "interrogation": interrogation,
            "prosecution": prosecution,
            "final_verdict": verdict,
            "processing_time_seconds": round(time.time() - start_time, 2),
        }

    def _error_response(self, error_msg: str, start_time: float) -> dict:
        return {"prosecution": {}, "final_verdict": {}, "model_used": self.model,
                "processing_time_seconds": round(time.time() - start_time, 2),
                "success": False, "error": error_msg}
