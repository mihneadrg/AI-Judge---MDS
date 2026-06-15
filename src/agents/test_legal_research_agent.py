"""
Teste pentru LegalResearchAgent și integrarea lui în CourtPipeline.

Acoperă:
- Unit tests pentru LegalResearchAgent (cu mock pentru apelul LLM)
- Robustețe la JSON invalid / input invalid (fallback gracios)
- Integration test: pipeline-ul expune `legal_article` după verdict
- Reziliență: o eroare la documentarea juridică NU compromite verdictul

Rulare:
    pytest src/agents/test_legal_research_agent.py -v
"""

import json
from unittest.mock import patch, MagicMock


# ─── Fixture-uri ─────────────────────────────────────────────────────────────

VALID_LEGAL_ARTICLE_JSON = {
    "law_code": "Codul Penal al României",
    "article_number": "Art. 228",
    "article_title": "Furtul",
    "article_text": (
        "Luarea unui bun mobil din posesia altuia, fără consimțământ, "
        "în scopul de a și-l însuși pe nedrept."
    ),
    "relevance": "Fapta descrisă corespunde elementelor constitutive ale furtului.",
    "disclaimer": "Informație juridică orientativă, nu constituie consultanță juridică.",
}

VALID_PROSECUTION = {
    "case_type": "Furt",
    "severity_level": "MODERATE",
    "formal_charges": ["Sustragerea unui bun mobil"],
    "evidence_list": ["Martori oculari"],
    "prosecution_summary": "Inculpatul a sustras un bun.",
    "original_input": "Mi-a furat bicicleta din fața blocului",
}

VALID_VERDICT = {
    "case_title": "Statul vs. Hoțul de Biciclete",
    "charges": "Sustragerea unui bun mobil",
    "evidence_presented": "Dovezi privind sustragerea",
    "legal_precedent": "Popescu vs. Bicicletă (1923)",
    "verdict": "VINOVAT",
    "sentence": "Restituirea bunului și 20 de ore de muncă în folosul comunității",
    "legal_reasoning": "Dovezile arată sustragerea cu intenție.",
    "courts_final_words": "Curtea se ridică!",
}


def make_mock_llm(response_dict: dict):
    """Mock pentru _call_ollama care returnează JSON-ul dat ca string."""
    return MagicMock(return_value=json.dumps(response_dict))


# ════════════════════════════════════════════════════════════════════════════
# TESTS: LegalResearchAgent
# ════════════════════════════════════════════════════════════════════════════

class TestLegalResearchAgent:

    def setup_method(self):
        from src.agents.legal_research_agent import LegalResearchAgent
        self.agent = LegalResearchAgent(model="llama3")

    def test_output_has_all_required_fields(self):
        """Eval: output-ul conține toate câmpurile necesare."""
        with patch.object(self.agent, "_call_ollama", make_mock_llm(VALID_LEGAL_ARTICLE_JSON)):
            result = self.agent.run({"verdict": VALID_VERDICT, "prosecution": VALID_PROSECUTION})

        required = [
            "law_code", "article_number", "article_title", "article_text",
            "relevance", "disclaimer", "agent", "model_used",
        ]
        for field in required:
            assert field in result, f"Câmpul '{field}' lipsește din output"

    def test_agent_field_is_correct(self):
        """Eval: câmpul 'agent' identifică corect agentul."""
        with patch.object(self.agent, "_call_ollama", make_mock_llm(VALID_LEGAL_ARTICLE_JSON)):
            result = self.agent.run({"verdict": VALID_VERDICT, "prosecution": VALID_PROSECUTION})

        assert result["agent"] == "LegalResearchAgent"

    def test_returns_expected_article(self):
        """Eval: câmpurile reflectă articolul returnat de model."""
        with patch.object(self.agent, "_call_ollama", make_mock_llm(VALID_LEGAL_ARTICLE_JSON)):
            result = self.agent.run({"verdict": VALID_VERDICT, "prosecution": VALID_PROSECUTION})

        assert result["article_number"] == "Art. 228"
        assert result["article_title"] == "Furtul"
        assert "Codul Penal" in result["law_code"]

    def test_accepts_string_input(self):
        """Eval: agentul acceptă și un string liber, nu doar dict."""
        with patch.object(self.agent, "_call_ollama", make_mock_llm(VALID_LEGAL_ARTICLE_JSON)):
            result = self.agent.run("Mi-a furat bicicleta")

        assert isinstance(result, dict)
        assert result["article_number"] == "Art. 228"

    def test_disclaimer_is_present(self):
        """Eval: răspunsul include mereu un disclaimer (nu e consultanță juridică)."""
        with patch.object(self.agent, "_call_ollama", make_mock_llm(VALID_LEGAL_ARTICLE_JSON)):
            result = self.agent.run({"verdict": VALID_VERDICT, "prosecution": VALID_PROSECUTION})

        assert result["disclaimer"]
        assert isinstance(result["disclaimer"], str)

    def test_invalid_json_uses_fallback(self):
        """Robustețe: JSON invalid de la model → fallback gracios, fără excepție."""
        with patch.object(self.agent, "_call_ollama", MagicMock(return_value="Nu sunt JSON.")):
            result = self.agent.run({"verdict": VALID_VERDICT, "prosecution": VALID_PROSECUTION})

        assert isinstance(result, dict)
        assert "article_number" in result
        assert result["agent"] == "LegalResearchAgent"

    def test_partial_json_uses_defaults(self):
        """Robustețe: JSON parțial → câmpurile lipsă primesc valori default."""
        with patch.object(self.agent, "_call_ollama", make_mock_llm({"article_number": "Art. 193"})):
            result = self.agent.run({"verdict": VALID_VERDICT, "prosecution": VALID_PROSECUTION})

        assert result["article_number"] == "Art. 193"
        assert "article_title" in result  # default aplicat
        assert "disclaimer" in result

    def test_invalid_input_returns_fallback(self):
        """Robustețe: input invalid (None) → fallback cu câmp de eroare."""
        result = self.agent.run(None)

        assert isinstance(result, dict)
        assert "article_number" in result
        assert "error" in result


# ════════════════════════════════════════════════════════════════════════════
# TESTS: Integrarea în CourtPipeline
# ════════════════════════════════════════════════════════════════════════════

class TestPipelineLegalArticle:

    def setup_method(self):
        from src.agents.pipeline import CourtPipeline
        self.pipeline = CourtPipeline(model="llama3")

    def test_judge_result_includes_legal_article(self):
        """Integration: rezultatul pipeline-ului conține `legal_article` după verdict."""
        with patch.object(self.pipeline.prosecutor, "_call_ollama", make_mock_llm(VALID_PROSECUTION)), \
             patch.object(self.pipeline.judge_agent, "_call_ollama", make_mock_llm(VALID_VERDICT)), \
             patch.object(self.pipeline.legal_researcher, "_call_ollama",
                          make_mock_llm(VALID_LEGAL_ARTICLE_JSON)):
            result = self.pipeline.judge("Mi-a furat bicicleta din fața blocului")

        assert result["success"] is True
        assert "legal_article" in result
        assert result["legal_article"]["article_number"] == "Art. 228"

    def test_legal_research_failure_does_not_break_verdict(self):
        """Reziliență: dacă documentarea juridică eșuează, verdictul rămâne valid."""
        with patch.object(self.pipeline.prosecutor, "_call_ollama", make_mock_llm(VALID_PROSECUTION)), \
             patch.object(self.pipeline.judge_agent, "_call_ollama", make_mock_llm(VALID_VERDICT)), \
             patch.object(self.pipeline.legal_researcher, "_call_ollama",
                          MagicMock(side_effect=ConnectionError("Model offline"))):
            result = self.pipeline.judge("Mi-a furat bicicleta")

        assert result["success"] is True
        assert "legal_article" in result
        # Fallback gracios cu marcaj de eroare
        assert "error" in result["legal_article"]
