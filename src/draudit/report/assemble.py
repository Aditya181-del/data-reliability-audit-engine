import hashlib
from datetime import datetime
from typing import List

from draudit.core.types import DatasetSnapshot
from draudit.metadata.resolution import UnassessedRisk
from draudit.diagnostics.types import StructuralRisk, RiskSeverity
from draudit.diagnostics.decision import AuditDecision
from draudit.report.model import AuditReport, AuditSummary


def _generate_audit_id(
    snapshot: DatasetSnapshot,
    decision: AuditDecision,
) -> str:
    """
    Generate a stable audit identifier based on immutable inputs.
    """

    payload = f"{snapshot.snapshot_id}:{decision.value}"
    return hashlib.sha256(payload.encode()).hexdigest()


def assemble_audit_report(
    *,
    snapshot: DatasetSnapshot,
    unassessed_risks: List[UnassessedRisk],
    structural_risks: List[StructuralRisk],
    decision: AuditDecision,
) -> AuditReport:
    """
    Assemble a complete audit report from precomputed components.

    This function contains no diagnostics and no business logic.
    """

    high_severity_count = sum(
        1 for r in structural_risks if r.severity == RiskSeverity.HIGH
    )

    summary = AuditSummary(
        decision=decision,
        total_unassessed_risks=len(unassessed_risks),
        total_structural_risks=len(structural_risks),
        high_severity_risks=high_severity_count,
    )

    audit_id = _generate_audit_id(snapshot, decision)

    return AuditReport(
        audit_id=audit_id,
        generated_at=datetime.utcnow(),
        dataset_snapshot=snapshot,
        unassessed_risks=unassessed_risks,
        structural_risks=structural_risks,
        decision=decision,
        summary=summary,
    )
