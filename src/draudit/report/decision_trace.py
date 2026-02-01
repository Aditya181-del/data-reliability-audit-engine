from dataclasses import dataclass
from typing import List

from draudit.diagnostics.decision import AuditDecision
from draudit.diagnostics.types import StructuralRisk, RiskSeverity, RiskConfidence
from draudit.metadata.resolution import UnassessedRisk


@dataclass(frozen=True)
class DecisionRuleTrace:
    rule_id: str
    description: str
    triggered: bool
    evidence: str


@dataclass(frozen=True)
class DecisionExplanation:
    decision: AuditDecision
    rule_traces: List[DecisionRuleTrace]
    summary: str


def build_decision_explanation(
    *,
    decision: AuditDecision,
    unassessed_risks: List[UnassessedRisk],
    structural_risks: List[StructuralRisk],
) -> DecisionExplanation:
    """
    Build a human-readable, auditable explanation for the final decision.
    """

    traces: List[DecisionRuleTrace] = []

    # Rule 1: Epistemic blockers
    traces.append(
        DecisionRuleTrace(
            rule_id="R1_EPISTEMIC_BLOCKER",
            description="Unassessed epistemic risks block safe progression.",
            triggered=bool(unassessed_risks),
            evidence=f"{len(unassessed_risks)} unassessed risks detected.",
        )
    )

    # Rule 2: Deterministic catastrophic failure
    catastrophic = [
        r
        for r in structural_risks
        if r.severity == RiskSeverity.HIGH and r.confidence == RiskConfidence.HIGH
    ]
    traces.append(
        DecisionRuleTrace(
            rule_id="R2_DETERMINISTIC_CATASTROPHE",
            description="High-severity, high-confidence deterministic risks require abort.",
            triggered=bool(catastrophic),
            evidence=f"{len(catastrophic)} catastrophic risks detected.",
        )
    )

    # Rule 3: High severity but uncertain
    uncertain_high = [
        r
        for r in structural_risks
        if r.severity == RiskSeverity.HIGH and r.confidence != RiskConfidence.HIGH
    ]
    traces.append(
        DecisionRuleTrace(
            rule_id="R3_HIGH_SEVERITY_UNCERTAIN",
            description="High-severity risks with uncertainty require fixing before proceeding.",
            triggered=bool(uncertain_high),
            evidence=f"{len(uncertain_high)} high-severity uncertain risks detected.",
        )
    )

    # Rule 4: Accumulated medium risks
    medium_count = sum(1 for r in structural_risks if r.severity == RiskSeverity.MEDIUM)
    traces.append(
        DecisionRuleTrace(
            rule_id="R4_ACCUMULATED_MEDIUM",
            description="Multiple medium-severity risks accumulate into significant concern.",
            triggered=medium_count >= 3,
            evidence=f"{medium_count} medium-severity risks detected.",
        )
    )

    # Rule 5: Probabilistic ceiling
    probabilistic = [
        r for r in structural_risks if r.risk_id.startswith("PROBABILISTIC_")
    ]
    traces.append(
        DecisionRuleTrace(
            rule_id="R5_PROBABILISTIC_CEILING",
            description="Probabilistic risks require review but cannot cause abort alone.",
            triggered=bool(probabilistic),
            evidence=f"{len(probabilistic)} probabilistic risks detected.",
        )
    )

    # Human summary (plain language)
    summary = (
        f"Final decision: {decision.value.upper()}. "
        "This decision was produced deterministically based on explicit escalation rules. "
        "Human review is required before any action is taken."
    )

    return DecisionExplanation(
        decision=decision,
        rule_traces=traces,
        summary=summary,
    )
