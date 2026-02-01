from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RiskSeverity(Enum):
    """
    How dangerous a detected issue is if left unresolved.
    """

    LOW = "low"  # Cosmetic or informational
    MEDIUM = "medium"  # Can degrade model reliability
    HIGH = "high"  # Likely to cause misleading outcomes


class RiskConfidence(Enum):
    """
    How confident the system is in the diagnosis itself.
    """

    LOW = "low"  # Weak signal or small sample size
    MEDIUM = "medium"  # Reasonable evidence
    HIGH = "high"  # Deterministic or overwhelming evidence


@dataclass(frozen=True)
class StructuralRisk:
    """
    A deterministic, explainable structural risk detected in the dataset.

    This represents an *observed fact*, not a hypothesis.
    """

    risk_id: str  # Stable identifier (e.g. DUPLICATE_ROWS)
    description: str  # Human-readable explanation
    affected_columns: Optional[list[str]]
    severity: RiskSeverity
    confidence: RiskConfidence
    evidence: str  # Concrete justification (counts, ratios, etc.)
