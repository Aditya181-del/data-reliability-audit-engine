from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

from draudit.core.types import DatasetSnapshot
from draudit.metadata.resolution import UnassessedRisk
from draudit.diagnostics.types import StructuralRisk
from draudit.diagnostics.decision import AuditDecision


@dataclass(frozen=True)
class AuditSummary:
    decision: AuditDecision
    total_unassessed_risks: int
    total_structural_risks: int
    high_severity_risks: int


@dataclass(frozen=True)
class AuditReport:
    """
    Immutable, authoritative audit output.

    🚫 NO explanation logic
    🚫 NO LLM coupling
    """

    audit_id: str
    generated_at: datetime

    dataset_snapshot: DatasetSnapshot

    unassessed_risks: List[UnassessedRisk]
    structural_risks: List[StructuralRisk]

    decision: AuditDecision
    summary: AuditSummary

    notes: Optional[str] = None

    # ------------------------------------------------------------------
    # Canonical serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "audit_id": self.audit_id,
            "generated_at": self.generated_at.isoformat(),
            "dataset_snapshot": asdict(self.dataset_snapshot),
            "unassessed_risks": [asdict(r) for r in self.unassessed_risks],
            "structural_risks": [
                {
                    **asdict(r),
                    "severity": r.severity.value,
                    "confidence": r.confidence.value,
                }
                for r in self.structural_risks
            ],
            "decision": self.decision.value,
            "summary": {
                "decision": self.summary.decision.value,
                "total_unassessed_risks": self.summary.total_unassessed_risks,
                "total_structural_risks": self.summary.total_structural_risks,
                "high_severity_risks": self.summary.high_severity_risks,
            },
            "notes": self.notes,
        }
