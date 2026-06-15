"""
Agents module — The Dramatic AI Court of Justice

Conține agenții AI și orchestratorul pipeline-ului:
    - ProsecutorAgent: Analizează situația și construiește dosarul de acuzare
    - JudgeAgent: Pronunță verdictul dramatic final
    - LegalResearchAgent: Caută articolul de lege real care fundamentează verdictul
    - CourtPipeline: Orchestrează fluxul complet între agenți
"""

from .prosecutor_agent import ProsecutorAgent
from .judge_agent import JudgeAgent
from .legal_research_agent import LegalResearchAgent
from .pipeline import CourtPipeline

__all__ = ["ProsecutorAgent", "JudgeAgent", "LegalResearchAgent", "CourtPipeline"]
