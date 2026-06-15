"""
Complainant Agent - Agentul Reclamant pentru modul Watch.
Generează o situație aleatorie și răspunde coerent la întrebările Interogatorului.
"""

from .base_agent import BaseAgent


SITUATION_GENERATOR_PROMPT = """You are a creative writer for a dramatic AI courtroom comedy show set in Romania.
Generate a random, specific, comedic everyday complaint for someone to bring to court.

CRITICAL: Respond with ONLY a valid JSON object. No text before or after. No markdown.
IMPORTANT: Write ALL text values in Romanian language.

The JSON must have exactly these fields:
{
  "situation": "O plângere vie și specifică (3-5 propoziții în română). Trebuie să includă: numele persoanelor implicate, un loc specific, ore/date exacte, ce s-a întâmplat și de ce reclamantul este furios. Absurdă dar credibilă.",
  "complainant_name": "Un nume românesc dramatic/amuzant (ex: Gheorghe Supărat-Rău, Maria Mânioasă, Constantin cel Jignit)"
}

Examples of good situations (in Romanian):
- Dispute cu vecinii (zgomot, parcare, animale, proprietate)
- Drame mărunte la locul de muncă (prânz furat, merit nerecunoscut)
- Certuri de familie pentru moșteniri bizare
- Conflicte cu business-uri pentru politici ridicole
- Războaie între colegi de apartament
- Dispute legate de pariuri sportive sau jocuri

Rules:
- Detalii specifice: nume românești reale, locuri reale din România, ore exacte
- Comic dar nu ofensator
- Reclamantul ar trebui să fie cel puțin parțial vinovat sau exagerat de dramatic
- Doar dispute civile cotidiene — fără infracțiuni grave
"""


ANSWER_SYSTEM_PROMPT_TEMPLATE = (
    'Ești {name}, un reclamant extrem de dramatic care a depus o plângere la curte.\n'
    'Plângerea ta: "{situation}"\n\n'
    'Ești interogat de INCHIZITORUL SEVERUS. Răspunde la întrebări sincer dar dramatic.\n\n'
    'CRITIC: Răspunde DOAR cu un obiect JSON valid. Fără text înainte sau după. Fără markdown.\n'
    'IMPORTANT: Scrie toate valorile în limba română.\n\n'
    'JSON-ul trebuie să aibă exact aceste câmpuri:\n'
    '{{"answer": "Răspunsul tău (2-4 propoziții). Specific, consistent cu plângerea, dramatic. Nu te contrazice."}}'
)


class ComplainantAgent(BaseAgent):
    """
    Agentul Reclamant — folosit în modul Watch pentru a juca rolul omului.

    Responsabilități:
    1. generate_situation() → inventează o plângere aleatorie cu detalii specifice
    2. answer_question()    → răspunde la întrebările Interogatorului rămânând în personaj
    """

    def __init__(self, model: str = "llama3", temperature: float = 0.9):
        super().__init__(model=model, temperature=temperature)

    def generate_situation(self) -> dict:
        """
        Generează o situație aleatorie pentru modul Watch.

        Returns:
            { "situation": str, "complainant_name": str }
        """
        raw = self._call_ollama(
            SITUATION_GENERATOR_PROMPT,
            "Generate a brand new dramatic court complaint now. Be creative and very specific!"
        )
        parsed = self._safe_parse_json(raw)

        if not parsed:
            return {
                "situation": (
                    "Vecinul meu, Gică Bătăios, îmi parchează mașina exact cu 3 centimetri "
                    "peste linia de demarcație a locului meu de parcare în fiecare dimineață "
                    "de la 4 martie încoace. Am măsurat. Am fotografii. Marți la 8:47 a făcut-o "
                    "DIN NOU și a avut obrăznicia să-mi facă cu mâna. Cer dreptate!"
                ),
                "complainant_name": "Maria Indignată-Rău",
            }

        return {
            "situation": parsed.get("situation", "An unspecified injustice has occurred."),
            "complainant_name": parsed.get("complainant_name", "Anonymous Complainant"),
        }

    def answer_question(
        self,
        situation: str,
        complainant_name: str,
        question: str,
        qa_history: list,
    ) -> dict:
        """
        Răspunde la o întrebare a Interogatorului rămânând în personaj.

        Returns:
            { "answer": str }
        """
        history_text = ""
        if qa_history:
            history_text = "\n\nPrevious questions you already answered:\n"
            for q, a in qa_history:
                history_text += f"Q: {q}\nYour answer: {a}\n"

        system_prompt = ANSWER_SYSTEM_PROMPT_TEMPLATE.format(
            name=complainant_name,
            situation=situation,
        )
        user_message = (
            f"The court asks you: {question}"
            f"{history_text}"
            "\n\nAnswer in character. Be consistent with your story. JSON only."
        )

        raw = self._call_ollama(system_prompt, user_message)
        parsed = self._safe_parse_json(raw)

        if not parsed:
            return {"answer": "Susțin tot ce am spus, Onorată Instanță! Fiecare cuvânt este adevărul!"}

        return {"answer": parsed.get("answer", "Nu pot spune mai mult în acest moment, Onorată Instanță!")}

    def run(self, input_data) -> dict:
        """Implementare cerută de BaseAgent. Delegă la generate sau answer."""
        if isinstance(input_data, dict) and "question" in input_data:
            return self.answer_question(
                situation=input_data.get("situation", ""),
                complainant_name=input_data.get("complainant_name", "Anonymous"),
                question=input_data.get("question", ""),
                qa_history=input_data.get("qa_history", []),
            )
        return self.generate_situation()
