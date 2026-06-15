"""
Teste automate și evals pentru sistemul de agenți.

Acoperă:
- Unit tests pentru ProsecutorAgent și JudgeAgent (cu mock Ollama)
- Evals pentru calitatea output-ului (structură, câmpuri, validitate)
- Integration test pentru CourtPipeline

Rulare:
    pytest tests/test_agents.py -v
    pytest tests/test_agents.py -v --tb=short  # output mai scurt
"""

import json
from unittest.mock import patch, MagicMock


# ─── Fixture-uri cu răspunsuri mock de la Ollama ────────────────────────────

VALID_PROSECUTION_JSON = {
    "case_type": "Domestic Disturbance",
    "severity_level": "SEVERE",
    "formal_charges": [
        "Willful and Malicious Midnight Guitar Playing in flagrante delicto",
        "Reckless Endangerment of Neighborhood Sleep Cycles",
        "Criminal Neglect of Common Decency Statutes",
    ],
    "evidence_list": [
        "Acoustic guitar heard at 3:00 AM by multiple witnesses",
        "Volume levels exceeding acceptable nocturnal thresholds",
        "Defendant showed no remorse when confronted",
    ],
    "prosecution_summary": "The accused did willfully and with malice aforethought disturb the peace of an entire neighborhood.",
    "recommended_sentence_hint": "A sentence befitting such nocturnal crimes must be considered.",
}

VALID_VERDICT_JSON = {
    "case_title": "Statul vs. Asasinul cu Chitara de Noapte",
    "charges": "Trei capete de acuzare pentru tulburarea liniștii publice",
    "evidence_presented": "Curtea a examinat dovezi acustice substanțiale ale faptei",
    "legal_precedent": "Liniște vs. Cacofonie (1923) — hotărârea de referință privind pacea nocturnă",
    "verdict": "VINOVAT",
    "sentence": "Inculpatul trebuie să participe la 40 de ore de meditație obligatorie în tăcere",
    "legal_reasoning": "Dovezile sunt copleșitoare. Disprețul inculpatului față de somn este fără precedent.",
    "courts_final_words": "Să fie acesta un avertisment pentru toți muzicienii nocturni! Curtea se ridică!",
}


# ─── Helper ─────────────────────────────────────────────────────────────────

def make_mock_ollama(response_dict: dict):
    """Creează un mock pentru _call_ollama care returnează JSON-ul dat."""
    mock = MagicMock(return_value=json.dumps(response_dict))
    return mock


# ════════════════════════════════════════════════════════════════════════════
# TESTS: ProsecutorAgent
# ════════════════════════════════════════════════════════════════════════════

class TestProsecutorAgent:

    def setup_method(self):
        """Importăm agenții înainte de fiecare test."""
        from src.agents.prosecutor_agent import ProsecutorAgent
        self.agent = ProsecutorAgent(model="llama3")

    # ── Structura output-ului ────────────────────────────────────────────────

    def test_output_has_all_required_fields(self):
        """Eval: output-ul conține toate câmpurile necesare."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_PROSECUTION_JSON)):
            result = self.agent.run("Vecinul cântă la 3 noaptea")

        required_fields = [
            "case_type", "severity_level", "formal_charges",
            "evidence_list", "prosecution_summary", "recommended_sentence_hint",
            "agent", "model_used",
        ]
        for field in required_fields:
            assert field in result, f"Câmpul '{field}' lipsește din output"

    def test_formal_charges_is_list(self):
        """Eval: acuzațiile sunt returnate ca listă."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_PROSECUTION_JSON)):
            result = self.agent.run("Colegul a mâncat peștele meu")

        assert isinstance(result["formal_charges"], list)
        assert len(result["formal_charges"]) > 0

    def test_evidence_list_is_list(self):
        """Eval: probele sunt returnate ca listă."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_PROSECUTION_JSON)):
            result = self.agent.run("Colegul a mâncat peștele meu")

        assert isinstance(result["evidence_list"], list)
        assert len(result["evidence_list"]) > 0

    def test_severity_level_is_valid(self):
        """Eval: severity_level are o valoare validă."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_PROSECUTION_JSON)):
            result = self.agent.run("Situație gravă")

        valid_levels = {"PETTY", "MODERATE", "SEVERE", "CATASTROPHIC"}
        assert result["severity_level"] in valid_levels, (
            f"severity_level '{result['severity_level']}' nu este valid"
        )

    def test_agent_field_is_correct(self):
        """Eval: câmpul 'agent' identifică corect agentul."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_PROSECUTION_JSON)):
            result = self.agent.run("Test")

        assert result["agent"] == "ProsecutorAgent"

    # ── Robustețe la input-uri problematice ─────────────────────────────────

    def test_empty_input_returns_error(self):
        """Robustețe: input gol returnează eroare gracioasă."""
        result = self.agent.run("")
        assert "error" in result or result.get("case_type") == "Unclassified Misconduct"

    def test_whitespace_input_returns_error(self):
        """Robustețe: input cu doar spații returnează eroare gracioasă."""
        result = self.agent.run("   ")
        assert "error" in result or result.get("case_type") == "Unclassified Misconduct"

    def test_invalid_json_from_model_uses_fallback(self):
        """Robustețe: dacă modelul nu returnează JSON valid, se folosește fallback."""
        with patch.object(self.agent, "_call_ollama", MagicMock(return_value="Acesta nu este JSON!")):
            result = self.agent.run("O situație")

        # Nu trebuie să crape — returnează fallback
        assert isinstance(result, dict)
        assert "formal_charges" in result
        assert isinstance(result["formal_charges"], list)

    def test_partial_json_from_model_uses_defaults(self):
        """Robustețe: JSON parțial (lipsesc câmpuri) → câmpuri default."""
        partial_json = {"case_type": "Test Case"}  # lipsesc celelalte câmpuri
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(partial_json)):
            result = self.agent.run("Test")

        assert result["case_type"] == "Test Case"
        assert "formal_charges" in result  # default aplicat
        assert isinstance(result["formal_charges"], list)

    def test_very_long_input(self):
        """Robustețe: input foarte lung nu crăpă agentul."""
        long_input = "Vecinul meu " * 200  # ~2400 cuvinte
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_PROSECUTION_JSON)):
            result = self.agent.run(long_input)

        assert isinstance(result, dict)
        assert "formal_charges" in result

    def test_special_characters_in_input(self):
        """Robustețe: caractere speciale în input nu crăpă agentul."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_PROSECUTION_JSON)):
            result = self.agent.run('Input cu "ghilimele" și \nnewlines și emoji 🎸')

        assert isinstance(result, dict)


# ════════════════════════════════════════════════════════════════════════════
# TESTS: JudgeAgent
# ════════════════════════════════════════════════════════════════════════════

class TestJudgeAgent:

    def setup_method(self):
        from src.agents.judge_agent import JudgeAgent
        self.agent = JudgeAgent(model="llama3")

    # ── Structura output-ului ────────────────────────────────────────────────

    def test_output_has_all_8_required_fields(self):
        """Eval: output-ul conține exact cele 8 câmpuri cerute în barem."""
        prosecution_input = {**VALID_PROSECUTION_JSON, "original_input": "Test", "raw_response": ""}
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_VERDICT_JSON)):
            result = self.agent.run(prosecution_input)

        required_fields = [
            "case_title", "charges", "evidence_presented", "legal_precedent",
            "verdict", "sentence", "legal_reasoning", "courts_final_words",
        ]
        for field in required_fields:
            assert field in result, f"Câmpul '{field}' lipsește din verdict"

    def test_verdict_is_vinovat_or_nevinovat(self):
        """Eval: verdictul este VINOVAT sau NEVINOVAT."""
        prosecution_input = {**VALID_PROSECUTION_JSON, "original_input": "Test", "raw_response": ""}
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_VERDICT_JSON)):
            result = self.agent.run(prosecution_input)

        assert result["verdict"] in {"VINOVAT", "NEVINOVAT"}, (
            f"Verdict invalid: '{result['verdict']}'"
        )

    def test_verdict_normalization_vinovat(self):
        """Eval: variante de VINOVAT sunt normalizate corect."""
        guilty_variants = [
            "VINOVAT", "vinovat", "Vinovat", "GUILTY", "guilty",
            "Inculpatul este VINOVAT dincolo de orice dubiu",
        ]
        for variant in guilty_variants:
            assert self.agent._normalize_verdict(variant) == "VINOVAT", (
                f"'{variant}' nu a fost normalizat la VINOVAT"
            )

    def test_verdict_normalization_nevinovat(self):
        """Eval: variante de NEVINOVAT sunt normalizate corect."""
        not_guilty_variants = [
            "NEVINOVAT", "nevinovat", "NOT GUILTY", "INNOCENT", "ACHITAT",
            "Inculpatul este NEVINOVAT",
        ]
        for variant in not_guilty_variants:
            assert self.agent._normalize_verdict(variant) == "NEVINOVAT", (
                f"'{variant}' nu a fost normalizat la NEVINOVAT"
            )

    def test_accepts_dict_input(self):
        """Eval: JudgeAgent acceptă dict de la ProsecutorAgent."""
        prosecution_dict = {**VALID_PROSECUTION_JSON, "original_input": "Test", "raw_response": ""}
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_VERDICT_JSON)):
            result = self.agent.run(prosecution_dict)

        assert isinstance(result, dict)
        assert "verdict" in result

    def test_accepts_string_input_standalone(self):
        """Eval: JudgeAgent funcționează și standalone cu string."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_VERDICT_JSON)):
            result = self.agent.run("Vecinul meu cântă noaptea")

        assert isinstance(result, dict)
        assert "verdict" in result

    def test_invalid_json_uses_fallback(self):
        """Robustețe: JSON invalid de la model → fallback gracioasă."""
        prosecution_input = {**VALID_PROSECUTION_JSON, "original_input": "Test", "raw_response": ""}
        with patch.object(self.agent, "_call_ollama", MagicMock(return_value="Nu sunt JSON.")):
            result = self.agent.run(prosecution_input)

        assert isinstance(result, dict)
        assert "verdict" in result
        assert result["verdict"] in {"VINOVAT", "NEVINOVAT"}

    def test_all_string_fields_are_non_empty(self):
        """Eval: câmpurile string din verdict nu sunt goale."""
        prosecution_input = {**VALID_PROSECUTION_JSON, "original_input": "Test", "raw_response": ""}
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_VERDICT_JSON)):
            result = self.agent.run(prosecution_input)

        string_fields = [
            "case_title", "charges", "evidence_presented", "legal_precedent",
            "verdict", "sentence", "legal_reasoning", "courts_final_words",
        ]
        for field in string_fields:
            assert result[field], f"Câmpul '{field}' este gol"
            assert isinstance(result[field], str), f"Câmpul '{field}' nu este string"


# ════════════════════════════════════════════════════════════════════════════
# TESTS: CourtPipeline (Integration)
# ════════════════════════════════════════════════════════════════════════════

class TestCourtPipeline:

    def setup_method(self):
        from src.agents.pipeline import CourtPipeline
        self.pipeline = CourtPipeline(model="llama3")

    def test_pipeline_returns_complete_result(self):
        """Integration: pipeline-ul returnează toate câmpurile așteptate."""
        with patch.object(self.pipeline.prosecutor, "_call_ollama",
                          make_mock_ollama(VALID_PROSECUTION_JSON)), \
             patch.object(self.pipeline.judge_agent, "_call_ollama",
                          make_mock_ollama(VALID_VERDICT_JSON)):
            result = self.pipeline.judge("Vecinul cântă noaptea")

        assert result["success"] is True
        assert "prosecution" in result
        assert "final_verdict" in result
        assert result["error"] is None

    def test_pipeline_result_has_prosecution_data(self):
        """Integration: rezultatul conține dosarul de la prosecutor."""
        with patch.object(self.pipeline.prosecutor, "_call_ollama",
                          make_mock_ollama(VALID_PROSECUTION_JSON)), \
             patch.object(self.pipeline.judge_agent, "_call_ollama",
                          make_mock_ollama(VALID_VERDICT_JSON)):
            result = self.pipeline.judge("Test situație")

        assert "case_type" in result["prosecution"]
        assert "formal_charges" in result["prosecution"]

    def test_pipeline_result_has_verdict_data(self):
        """Integration: rezultatul conține verdictul de la judge."""
        with patch.object(self.pipeline.prosecutor, "_call_ollama",
                          make_mock_ollama(VALID_PROSECUTION_JSON)), \
             patch.object(self.pipeline.judge_agent, "_call_ollama",
                          make_mock_ollama(VALID_VERDICT_JSON)):
            result = self.pipeline.judge("Test situație")

        assert "verdict" in result["final_verdict"]
        assert "case_title" in result["final_verdict"]

    def test_pipeline_empty_input_returns_error(self):
        """Robustețe: input gol → success=False cu mesaj de eroare."""
        result = self.pipeline.judge("")

        assert result["success"] is False
        assert result["error"] is not None
        assert result["prosecution"] == {}

    def test_pipeline_has_processing_time(self):
        """Integration: rezultatul include timpul de procesare."""
        with patch.object(self.pipeline.prosecutor, "_call_ollama",
                          make_mock_ollama(VALID_PROSECUTION_JSON)), \
             patch.object(self.pipeline.judge_agent, "_call_ollama",
                          make_mock_ollama(VALID_VERDICT_JSON)):
            result = self.pipeline.judge("Test")

        assert "processing_time_seconds" in result
        assert isinstance(result["processing_time_seconds"], float)
        assert result["processing_time_seconds"] >= 0

    def test_pipeline_prosecutor_failure_handled(self):
        """Robustețe: eroare la prosecutor → pipeline returnează eroare gracioasă."""
        with patch.object(self.pipeline.prosecutor, "_call_ollama",
                          MagicMock(side_effect=ConnectionError("Ollama offline"))):
            result = self.pipeline.judge("Test situație")

        assert result["success"] is False
        assert "Ollama" in result["error"] or result["error"] is not None

    def test_pipeline_uses_correct_model(self):
        """Integration: pipeline-ul raportează corect modelul folosit."""
        with patch.object(self.pipeline.prosecutor, "_call_ollama",
                          make_mock_ollama(VALID_PROSECUTION_JSON)), \
             patch.object(self.pipeline.judge_agent, "_call_ollama",
                          make_mock_ollama(VALID_VERDICT_JSON)):
            result = self.pipeline.judge("Test")

        assert result["model_used"] == "llama3"


# ════════════════════════════════════════════════════════════════════════════
# TESTS: BaseAgent utilities
# ════════════════════════════════════════════════════════════════════════════

class TestBaseAgentUtilities:

    def setup_method(self):
        from src.agents.prosecutor_agent import ProsecutorAgent
        # Folosim ProsecutorAgent pentru a testa metodele din BaseAgent
        self.agent = ProsecutorAgent(model="llama3")

    def test_safe_parse_valid_json(self):
        """Util: parsează corect JSON valid."""
        text = '{"key": "value", "number": 42}'
        result = self.agent._safe_parse_json(text)
        assert result == {"key": "value", "number": 42}

    def test_safe_parse_json_in_markdown_block(self):
        """Util: extrage JSON din bloc markdown ```json ... ```."""
        text = 'Iată răspunsul:\n```json\n{"key": "value"}\n```\nSper că ajută!'
        result = self.agent._safe_parse_json(text)
        assert result == {"key": "value"}

    def test_safe_parse_json_embedded_in_text(self):
        """Util: extrage JSON { } din text mixt."""
        text = 'Bla bla {"verdict": "GUILTY", "score": 10} bla bla'
        result = self.agent._safe_parse_json(text)
        assert result is not None
        assert result["verdict"] == "GUILTY"

    def test_safe_parse_invalid_json_returns_none(self):
        """Util: text fără JSON returnează None (nu crăpă)."""
        result = self.agent._safe_parse_json("Acesta nu conține JSON deloc.")
        assert result is None

    def test_safe_parse_empty_string(self):
        """Util: string gol returnează None."""
        result = self.agent._safe_parse_json("")
        assert result is None


# ════════════════════════════════════════════════════════════════════════════
# TESTS: ComplainantAgent
# ════════════════════════════════════════════════════════════════════════════

VALID_SITUATION_JSON = {
    "situation": (
        "Vecinul meu, Gică Bătăios, îmi parchează mașina exact cu 3 centimetri "
        "peste linia de demarcație a locului meu de parcare în fiecare dimineață "
        "de la 4 martie încoace. Marți la 8:47 a făcut-o DIN NOU!"
    ),
    "complainant_name": "Maria Indignată-Rău",
}

VALID_ANSWER_JSON = {
    "answer": (
        "Da, Onorată Instanță! Gică Bătăios a parcat iar cu 3 centimetri peste linie. "
        "Am fotografii, am martori și am chiar și o riglă cu care am măsurat!"
    ),
}


class TestComplainantAgent:

    def setup_method(self):
        from src.agents.complainant_agent import ComplainantAgent
        self.agent = ComplainantAgent(model="llama3", temperature=0.9)

    # ── generate_situation() ─────────────────────────────────────────────────

    def test_generate_situation_returns_dict(self):
        """Eval: generate_situation() returnează un dict."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_SITUATION_JSON)):
            result = self.agent.generate_situation()

        assert isinstance(result, dict)

    def test_generate_situation_has_required_fields(self):
        """Eval: generate_situation() conține câmpurile 'situation' și 'complainant_name'."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_SITUATION_JSON)):
            result = self.agent.generate_situation()

        assert "situation" in result, "Câmpul 'situation' lipsește"
        assert "complainant_name" in result, "Câmpul 'complainant_name' lipsește"

    def test_generate_situation_fields_are_non_empty_strings(self):
        """Eval: câmpurile returnate sunt stringuri non-goale."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_SITUATION_JSON)):
            result = self.agent.generate_situation()

        assert isinstance(result["situation"], str) and len(result["situation"]) > 0
        assert isinstance(result["complainant_name"], str) and len(result["complainant_name"]) > 0

    def test_generate_situation_fallback_on_invalid_json(self):
        """Robustețe: JSON invalid → fallback cu situație hardcodată."""
        with patch.object(self.agent, "_call_ollama", MagicMock(return_value="Nu sunt JSON!")):
            result = self.agent.generate_situation()

        assert isinstance(result, dict)
        assert "situation" in result
        assert "complainant_name" in result
        assert result["complainant_name"] == "Maria Indignată-Rău"

    def test_generate_situation_fallback_on_empty_response(self):
        """Robustețe: răspuns gol → fallback gracioasă."""
        with patch.object(self.agent, "_call_ollama", MagicMock(return_value="")):
            result = self.agent.generate_situation()

        assert isinstance(result, dict)
        assert "situation" in result
        assert len(result["situation"]) > 0

    # ── answer_question() ────────────────────────────────────────────────────

    def test_answer_question_returns_dict(self):
        """Eval: answer_question() returnează un dict."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_ANSWER_JSON)):
            result = self.agent.answer_question(
                situation="Vecinul parchează prost.",
                complainant_name="Maria Indignată-Rău",
                question="De cât timp se întâmplă asta?",
                qa_history=[],
            )

        assert isinstance(result, dict)

    def test_answer_question_has_answer_field(self):
        """Eval: answer_question() conține câmpul 'answer'."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_ANSWER_JSON)):
            result = self.agent.answer_question(
                situation="Vecinul parchează prost.",
                complainant_name="Maria Indignată-Rău",
                question="De cât timp se întâmplă asta?",
                qa_history=[],
            )

        assert "answer" in result
        assert isinstance(result["answer"], str)
        assert len(result["answer"]) > 0

    def test_answer_question_fallback_on_invalid_json(self):
        """Robustețe: JSON invalid la răspuns → fallback cu text hardcodat."""
        with patch.object(self.agent, "_call_ollama", MagicMock(return_value="Nu sunt JSON!")):
            result = self.agent.answer_question(
                situation="Test",
                complainant_name="Test Name",
                question="Test question?",
                qa_history=[],
            )

        assert isinstance(result, dict)
        assert "answer" in result
        assert len(result["answer"]) > 0

    def test_answer_question_with_qa_history(self):
        """Eval: answer_question() funcționează cu istoric de întrebări anterioare."""
        history = [
            ("Ce s-a întâmplat?", "Vecinul a parcat prost."),
            ("Ai martori?", "Da, doamna Popescu a văzut tot!"),
        ]
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_ANSWER_JSON)):
            result = self.agent.answer_question(
                situation="Vecinul parchează prost.",
                complainant_name="Maria",
                question="Mai ai ceva de adăugat?",
                qa_history=history,
            )

        assert isinstance(result, dict)
        assert "answer" in result

    def test_answer_question_with_empty_history(self):
        """Eval: answer_question() funcționează cu istoric gol."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_ANSWER_JSON)):
            result = self.agent.answer_question(
                situation="Situație de test",
                complainant_name="Ion Test",
                question="Prima întrebare?",
                qa_history=[],
            )

        assert "answer" in result

    # ── run() – delegare ─────────────────────────────────────────────────────

    def test_run_without_question_calls_generate_situation(self):
        """Eval: run() fără 'question' delegă la generate_situation()."""
        with patch.object(self.agent, "generate_situation",
                          MagicMock(return_value=VALID_SITUATION_JSON)) as mock_gen:
            self.agent.run({})

        mock_gen.assert_called_once()

    def test_run_with_question_calls_answer_question(self):
        """Eval: run() cu 'question' în dict delegă la answer_question()."""
        input_data = {
            "question": "De ce ai venit la curte?",
            "situation": "Vecinul parchează prost.",
            "complainant_name": "Maria",
            "qa_history": [],
        }
        with patch.object(self.agent, "answer_question",
                          MagicMock(return_value=VALID_ANSWER_JSON)) as mock_ans:
            self.agent.run(input_data)

        mock_ans.assert_called_once()

    def test_run_with_string_input_calls_generate_situation(self):
        """Eval: run() cu string (nu dict) delegă la generate_situation()."""
        with patch.object(self.agent, "generate_situation",
                          MagicMock(return_value=VALID_SITUATION_JSON)) as mock_gen:
            self.agent.run("ceva text")

        mock_gen.assert_called_once()

    def test_run_returns_dict(self):
        """Eval: run() returnează întotdeauna un dict."""
        with patch.object(self.agent, "_call_ollama", make_mock_ollama(VALID_SITUATION_JSON)):
            result = self.agent.run({})

        assert isinstance(result, dict)
