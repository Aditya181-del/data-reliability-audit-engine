# src/draudit/pipeline/schemas.py

from dataclasses import dataclass
from typing import Optional

from draudit.report.model import AuditReport
from draudit.explain.schemas import ExplanationResponse


@dataclass(frozen=True)
class AuditWithExplanation:
    """
    Final pipeline output.

    Combines:
    - Deterministic audit report
    - Optional non-authoritative LLM explanation
    """

    audit: AuditReport
    explanation: Optional[ExplanationResponse]
