"""
Agents module — The Dramatic AI Court of Justice

Conține cei doi agenți AI și orchestratorul pipeline-ului:
    - ProsecutorAgent: Analizează situația și construiește dosarul de acuzare
    - JudgeAgent: Pronunță verdictul dramatic final
    - CourtPipeline: Orchestrează fluxul complet între cei doi agenți
"""

from .prosecutor_agent import ProsecutorAgent
from .judge_agent import JudgeAgent
from .pipeline import CourtPipeline

__all__ = ["ProsecutorAgent", "JudgeAgent", "CourtPipeline"]
