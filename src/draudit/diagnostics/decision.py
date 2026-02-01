from enum import Enum
from typing import List

from draudit.diagnostics.types import StructuralRisk, RiskSeverity, RiskConfidence
from draudit.metadata.resolution import UnassessedRisk


class AuditDecision(Enum):
    """
    Final recommendation produced by the audit system.

    This is NOT an automated action.
    It is an explicit recommendation for human review.
    """

    PROCEED = "proceed"
    FIX = "fix"
    ABORT = "abort"


# Explicit list of probabilistic-only risk IDs
_PROBABILISTIC_RISK_IDS = {
    "PROBABILISTIC_DEPENDENCE_KS",
    "PROBABILISTIC_DEPENDENCE_CHI2",
}


def make_audit_decision(
    *,
    unassessed_risks: List[UnassessedRisk],
    structural_risks: List[StructuralRisk],
) -> AuditDecision:
    """
    Aggregate risks into a single audit decision.

    Properties:
    - Deterministic
    - Explainable
    - Non-autonomous
    - Governance-safe
    """

    # --------------------------------------------------
    # Rule 1: Epistemic uncertainty blocks progress
    # --------------------------------------------------
    if unassessed_risks:
        return AuditDecision.FIX

    # --------------------------------------------------
    # Separate deterministic vs probabilistic risks
    # --------------------------------------------------
    deterministic_risks = [
        r for r in structural_risks if r.risk_id not in _PROBABILISTIC_RISK_IDS
    ]

    probabilistic_risks = [
        r for r in structural_risks if r.risk_id in _PROBABILISTIC_RISK_IDS
    ]

    # --------------------------------------------------
    # Rule 2: Deterministic catastrophic failure → ABORT
    # --------------------------------------------------
    for r in deterministic_risks:
        if r.severity == RiskSeverity.HIGH and r.confidence == RiskConfidence.HIGH:
            return AuditDecision.ABORT

    # --------------------------------------------------
    # Rule 3: Deterministic but uncertain → FIX
    # --------------------------------------------------
    for r in deterministic_risks:
        if r.severity == RiskSeverity.HIGH:
            return AuditDecision.FIX

    # --------------------------------------------------
    # Rule 4: Accumulated medium risks → FIX
    # --------------------------------------------------
    medium_count = sum(1 for r in structural_risks if r.severity == RiskSeverity.MEDIUM)
    if medium_count >= 3:
        return AuditDecision.FIX

    # --------------------------------------------------
    # Rule 5: Probabilistic ceiling → FIX
    # --------------------------------------------------
    if probabilistic_risks:
        return AuditDecision.FIX

    # --------------------------------------------------
    # Rule 6: Clean bill of health → PROCEED
    # --------------------------------------------------
    return AuditDecision.PROCEED
